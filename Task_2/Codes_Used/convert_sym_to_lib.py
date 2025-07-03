import re

def parse_xschem_sym(sym_path):
    with open(sym_path, "r") as f:
        lines = f.readlines()

    symbol_name = None
    pins = []

    for line in lines:
        if "template=" in line:
            match = re.search(r'format="@(.*?)\\', line)
            if match:
                symbol_name = match.group(1)
        elif line.startswith("B"):
            info = re.search(r"name=([A-Za-z0-9_]+) dir=(in|out)", line)
            if info:
                pins.append({
                    "name": info.group(1),
                    "dir": info.group(2)
                })

    return symbol_name or "and2_1", pins

def generate_lib(symbol_name, pins, output_file):
    with open(output_file, "w") as f:
        f.write("EESchema-LIBRARY Version 2.3\n")
        f.write("#encoding utf-8\n")
        f.write(f"#\n# {symbol_name}\n#\n")
        f.write(f"DEF {symbol_name} U 0 40 Y Y 1 F N\n")
        f.write(f'F0 "U" 0 0 60 H V C CNN\n')
        f.write(f'F1 "{symbol_name}" 50 100 60 H V C CNN\n')
        f.write(f'F2 "" 0 0 60 H V C CNN\n')
        f.write(f'F3 "" 0 0 60 H V C CNN\n')
        f.write("DRAW\n")

        # Body of the symbol (rectangle and arc like AND gate)
        f.write("S -30 -30 5 30 0 1 10 N\n")
        f.write("L -60 -20 -30 -20 0 1 10 N\n")
        f.write("L -60 20 -30 20 0 1 10 N\n")
        f.write("L -30 -30 5 -30 0 1 10 N\n")
        f.write("L -30 30 5 30 0 1 10 N\n")
        f.write("A 0 0 30 270 180 0 1 0 N\n")

        # Pins
        x_in = -100
        y = -20
        spacing = 40
        pin_number = 1
        for pin in pins:
            if pin["dir"] == "in":
                f.write(f"X {pin['name']} {pin_number} {x_in} {y} 200 R 50 50 1 1 I\n")
                y += spacing
            pin_number += 1

        for pin in pins:
            if pin["dir"] == "out":
                f.write(f"X {pin['name']} {pin_number} 100 0 200 L 50 50 1 1 O\n")
                pin_number += 1

        f.write("ENDDRAW\nENDDEF\n")

# Example usage:
sym_file = "sg13g2_and2_1.sym"
symbol_name, pins = parse_xschem_sym(sym_file)
generate_lib(symbol_name, pins, "converted.lib")
