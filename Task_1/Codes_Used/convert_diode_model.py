import re  # Regular expressions module for pattern matching

# This function extracts only the necessary diode model parameters
# from an IHP .MODEL line and converts them into eSim-compatible format.
def extract_esim_model_params(model_line):
    """
    Extracts and converts diode model parameters to eSim-compatible format.
    Ignores parameters not supported in eSim like 'tnom', 'xti', 'eg', etc.
    """
    # Dictionary to map IHP parameter names to eSim-compatible ones
    param_map = {
        'is': 'is',     # Saturation current
        'rs': 'rs',     # Series resistance
        'n': 'n',       # Emission coefficient
        'tt': 'tt',     # Transit time
        'cjo': 'cjo',   # Junction capacitance
        'cj0': 'cjo',   # Alias for cjo
        'vj': 'vj',     # Junction potential
        'm': 'm',       # Grading coefficient
        'bv': 'bv',     # Breakdown voltage
        'ibv': 'ibv'    # Current at breakdown
    }

    # Remove ".MODEL" and the model name/type (e.g., D) from the beginning
    model_def = re.sub(r'^\.MODEL\s+\S+\s+\S+\s*\(', '', model_line.strip(), flags=re.IGNORECASE)
    model_def = model_def.rstrip(')')  # Remove the closing parenthesis at the end

    # Extract all key=value pairs from the line
    raw_params = re.findall(r'(\w+)\s*=\s*([^\s]+)', model_def)

    # Prepare a list to store only the parameters supported by eSim
    esim_params = []
    for key, value in raw_params:
        key_lower = key.lower()  # Convert key to lowercase for uniformity
        if key_lower in param_map:
            esim_key = param_map[key_lower]  # Get the mapped eSim key
            esim_params.append(f"{esim_key}={value}")  # Store in format key=value

    return esim_params

# This function converts the IHP PDK model file into an eSim-compatible format
def convert_ihp_to_esim(input_file, output_file):
    # Open the IHP model file and read all lines
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Open the output file where the eSim models will be written
    with open(output_file, 'w') as outfile:
        outfile.write("* eSim-Compatible Diode Models\n\n")

        # Loop through each line of the input file
        for line in lines:
            # Check if the line defines a diode model
            if line.strip().lower().startswith(".model") and "d" in line.lower():
                parts = line.split()
                if len(parts) < 3:
                    continue  # Skip if the line doesn't follow expected structure
                model_name = parts[1]  # Extract the name of the model

                # Get the list of compatible parameters
                esim_params = extract_esim_model_params(line)

                # Write the formatted model definition to the output file
                outfile.write(f".model {model_name} D(\n")
                for param in esim_params:
                    outfile.write(f"  {param}\n")
                outfile.write(")\n\n")

    # Notify user that the conversion is done
    print(f"✅ Converted model(s) written to: {output_file}")

# Run the function with given input and output file names
convert_ihp_to_esim("ihp_diode_model.spice.txt", "esim_diode_model.model")
