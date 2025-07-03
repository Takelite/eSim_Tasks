import re  # Importing the 're' module for regular expression operations


def parse_xschem_sym(sym_path):
    """
    Parses an xschem .sym file to extract the symbol name and pin information.

    Args:
        sym_path (str): Path to the .sym file.

    Returns:
        tuple: A tuple containing the symbol name (str) and a list of pin dictionaries.
    """
    with open(sym_path, "r") as f:
        lines = f.readlines()  # Read all lines of the .sym file

    symbol_name = None
    pins = []

    for line in lines:
        # Find the symbol name from a line that contains the template definition
        if "template=" in line:
            match = re.search(r'format="@(.*?)\\', line)
            if match:
                symbol_name = match.group(1)  # Extract the symbol name

        # Look for lines starting with "B" that define pins
        elif line.startswith("B"):
            # Extract pin name and direction (in or out)
            info = re.search(r"name=([A-Za-z0-9_]+) dir=(in|out)", line)
            if info:
                pins.append({
                    "name": info.group(1),
                    "dir": info.group(2)
                })

    # Return symbol name and pin list; default name is "and2_1" if none found
    return symbol_name or "and2_1", pins


def generate_lib(symbol_name, pins, output_file):
    """
    Generates a .lib file for eSim using symbol name and pin data.

    Args:
        symbol_name (str): Name of the symbol.
        pins (list): List of dictionaries with pin names and directions.
        output_file (str): Path to the output .lib file.
    """
    with open(output_file, "w") as f:
        # Write basic headers required for a KiCad/eSim .lib file
        f.write("EESchema-LIBRARY Version 2.3\n")
        f.write("#encoding utf-8\n")
        f.write(f"#\n# {symbol_name}\n#\n")
        f.write(f"DEF {symbol_name} U 0 40 Y Y 1 F N\n")
        f.write('F0 "U" 0 0 60 H V C CNN\n')
        f.write(f'F1 "{symbol_name}" 50 100 60 H V C CNN\n')
        f.write('F2 "" 0 0 60 H V C CNN\n')
        f.write('F3 "" 0 0 60 H V C CNN\n')
        f.write("DRAW\n")

        # Draw the body of the symbol (like a logic gate)
        f.write("S -30 -30 5 30 0 1 10 N\n")   # Rectangle part
        f.write("L -60 -20 -30 -20 0 1 10 N\n")  # Left side lines for pins
        f.write("L -60 20 -30 20 0 1 10 N\n")
        f.write("L -30 -30 5 -30 0 1 10 N\n")
        f.write("L -30 30 5 30 0 1 10 N\n")
        f.write("A 0 0 30 270 180 0 1 0 N\n")  # Arc for the AND gate shape

        # Initialize position for input pins
        x_in = -100  # X-coordinate for input pins (on the left)
        y = -20      # Y-coordinate starting point
        spacing = 40  # Vertical space between pins
        pin_number = 1

        # Add input pins from the parsed data
        for pin in pins:
            if pin["dir"] == "in":
                f.write(f"X {pin['name']} {pin_number} {x_in} {y} 200 R 50 50 1 1 I\n")
                y += spacing  # Move Y down for the next pin
                pin_number += 1

        # Add output pins to the right side of the symbol
        for pin in pins:
            if pin["dir"] == "out":
                f.write(f"X {pin['name']} {pin_number} 100 0 200 L 50 50 1 1 O\n")
                pin_number += 1

        # End the drawing section and definition
        f.write("ENDDRAW\nENDDEF\n")


# -------------------- Example Usage --------------------

# Provide the path to the input .sym file (from xschem)
sym_file = "sg13g2_and2_1.sym"

# Parse the symbol name and pins from the .sym file
symbol_name, pins = parse_xschem_sym(sym_file)

# Generate a .lib file using the parsed data
generate_lib(symbol_name, pins, "converted.lib")
