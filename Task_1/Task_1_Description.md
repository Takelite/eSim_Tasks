# Explanation of Code and Differences Between IHP PDK and eSim Formats

## Objective

The objective of this task was to convert SPICE model files provided by the IHP PDK into a format that is compatible with eSim. The Python script developed for this task specifically handles `.MODEL` definitions for diodes and reformats them for use within eSim’s simulation environment.

## Why Convert `.spice` to `.model`?

- The IHP PDK provides model definitions in `.spice` files, which are designed for use with commercial simulators (like Spectre or HSPICE). These models contain a wide range of parameters — some of which are too detailed or unsupported in eSim.
- eSim (based on Ngspice) requires a simpler format and supports only a limited set of parameters (like `is`, `n`, `rs`, `tt`, etc.).
- By converting `.spice` files to `.model` files, we:
  - Strip away unsupported or irrelevant parameters.
  - Reformat the model into a multi-line, readable format.
  - Ensure compatibility with eSim's simulator backend.
  - Create ready-to-import models for use in eSim schematic or netlist simulation.

## Key Differences Between IHP PDK and eSim

- **Parameter Scope:**  
  IHP PDK model files often contain detailed parameters meant for high-accuracy simulations in industrial tools. These include advanced temperature and semiconductor behavior parameters such as `tnom`, `xti`, `eg`, and others.

- **eSim Compatibility:**  
  eSim, which is built on Ngspice, supports a limited subset of these SPICE parameters. Including unsupported parameters can cause simulation errors or prevent the models from being loaded correctly.

- **Formatting Style:**  
  IHP model definitions are typically written as single-line entries. In contrast, eSim prefers multi-line, readable definitions which are easier to parse and debug.

- **Parameter Naming:**  
  Parameters in IHP files may appear in either uppercase or lowercase. To ensure consistency and compatibility, all keys were converted to lowercase during parsing.

- **Simplification Requirement:**  
  Many of the parameters included in IHP files are not necessary for typical eSim use cases. These were intentionally filtered out to produce a lightweight, compatible output.

## Script Design and Logic

- The script begins by opening and reading the input `.spice` file line by line.
- Only `.MODEL` lines that define diode models (`.MODEL <name> D(...)`) are processed. This filtering ensures that the output is limited to relevant device types.
- Regular expressions are used to extract key-value parameter pairs from the model definitions.
- A mapping dictionary defines allowed parameters that are supported by eSim (`is`, `rs`, `n`, `tt`, `cjo`, `vj`, `m`, `bv`, `ibv`). Parameters not found in this list are ignored.
- Equivalent aliases such as `cj0` and `cjo` are treated as the same during mapping.
- Each supported parameter is written into the output file in a clean, multi-line `.model` format.
- A header comment is included at the top of the output to indicate the file’s purpose and compatibility.

## How to Run the Script in VS Code

1. **Prepare the input file:**
   - Create or download a `.spice` file (e.g., `ihp_diode_model.spice.txt`) containing IHP diode `.MODEL` definitions.
   - Place this file in the same directory as your Python script (or adjust the path accordingly in the script).

2. **Open VS Code:**
   - Launch VS Code and open the folder containing your script and model file.

3. **Run the script:**
   - Open a terminal in VS Code (`` Ctrl + ` ``).
   - Run the script using:
     ```bash
     python convert_ihp_to_esim.py
     ```
   - Or modify the last line in the script to match your filename:
     ```python
     convert_ihp_to_esim("ihp_diode_model.spice.txt", "esim_diode_model.model")
     ```

4. **Check the Output:**
   - After running, you’ll get a file like `esim_diode_model.model`, ready for use in your eSim circuit netlists.

## Additional Features

- The script outputs eSim-compatible `.model` blocks that can be directly included in schematic simulations.
- It is generic enough to handle multiple diode models in a single file and can be extended for other device types (e.g., MOSFETs or BJTs) with minor changes in the filtering logic.
- By stripping unsupported and unnecessary parameters, the script ensures that the output remains compact, readable, and free of compatibility issues with eSim.

## Summary

This script acts as a translator between detailed SPICE model files from the IHP PDK and the streamlined format required by eSim. By extracting only supported parameters and reformatting them properly, it simplifies the model integration process for users and ensures successful simulation in the eSim environment. It is particularly useful for academic and open-source scenarios where ease of use and compatibility are key concerns.
