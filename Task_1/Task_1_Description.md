# Explanation of Code and Differences Between IHP PDK and eSim Formats

## Objective

The objective of this task was to convert SPICE model files provided by the IHP PDK into a format that is compatible with eSim. The Python script developed for this task specifically handles `.MODEL` definitions for diodes and reformats them for use within eSim’s simulation environment.

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

## How to Run the Script in VSCode

Follow these steps to run the script and generate an eSim-compatible `.model` file using Visual Studio Code:

### 1. Prepare the Files

- Ensure you have Python installed (preferably Python 3.x).
- Create a folder (e.g., `esim_converter`) and open it in VSCode.
- Inside this folder, add the following files:
  - `convert_model.py` — the Python script with the conversion logic.
  - `ihp_diode_model.spice.txt` — your input SPICE model file from the IHP PDK.

### 2. Open the Terminal

- In VSCode, go to the top menu and click on:
  - `Terminal > New Terminal`
- This opens a terminal at the bottom of the VSCode window, already set to your current working folder.
- Set the right directory with the `cd` command in the terminal, by adding the `.py` files in the same location as the path you provide.

### 3. Run the Script

- Type the following command in the terminal:
  ```bash
  python convert_model.py
or just click on the run button.

This should be sufficient to generate an eSim compatible `.model` file with the appropriate parameters taken care of.
