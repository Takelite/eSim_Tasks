# Task 3: Simulation Automation Tool

## Objective

The goal of Task 3 is to develop a **Python-based automation tool** that helps users easily set up and run circuit simulations using **eSim** and **Ngspice**, especially when working with **IHP PDK models**. This tool reduces the manual effort of editing `.cir` files and simplifies the overall simulation workflow.

---

## Understanding the Context

- **IHP PDK models** are professionally detailed and often require specific inclusion in the netlist.
- **eSim** uses **Ngspice** as its simulation engine and expects a `.cir` file with a `.control` block to perform simulations.
- Manually configuring these files for different types of simulations (DC, AC, Transient) can be tedious and error-prone, especially for beginners.

This script automates that process while ensuring compatibility with eSim and Ngspice.

---

## Key Functionalities of the Script

### 1. **User Input Handling**
- Prompts the user to provide:
  - Circuit file exported from eSim (`.cir`)
  - Optional `.lib` model file from IHP PDK
  - Simulation type: **DC**, **AC**, or **Transient (tran)**
  - Simulation parameters (e.g., sweep range, time step)
  - Output signals to plot (e.g., `v(out)`)

### 2. **Circuit File Modification**
- Reads the original `.cir` file.
- Optionally adds `.include "<path_to_lib>"` for IHP PDK model.
- Skips any existing `.control` blocks to avoid conflicts.
- Injects a fresh `.control` block with:
  - The correct simulation command (based on user input)
  - Plot command
  - Output to `.raw` file for waveform viewing

### 3. **Simulation Execution**
- Uses Python’s `subprocess` module to run:

  ```bash
  ngspice updated_<filename>.cir
  ```
### 🖴 Output

- Creates a modified netlist named `updated_<original>.cir`
- Generates a `simulation_output.raw` file containing waveform data
- Saves the simulation output (stdout and stderr) to `simulation_log.txt` for debugging

---

### How to Run the Script in VS Code

#### 1. Prepare Files
- Ensure your `.cir` file is exported from eSim and available in your project folder.
- If using a `.lib` model (e.g., from IHP PDK), place it in the same folder or note the full path.

#### 2. Open VS Code
- Open the folder containing the script and your `.cir` file.

#### 3. Run the Script
- Open a terminal in VS Code.
- Run the following command:

```bash
python3 simulation_automation.py
```

### 4. Follow the Prompts

- Enter the filename of the circuit (e.g., `inverter.cir`)
- Provide the model file path if needed (or press Enter to skip)
- Choose simulation type: `dc`, `tran`, or `ac`
- Enter simulation parameters and the output nodes to plot
- Wait for the script to complete

---

### 5. Check Outputs

- `updated_<your_circuit>.cir` — modified file ready to simulate
- `simulation_output.raw` — waveform data
- `simulation_log.txt` — Ngspice output and logs

---

### IHP PDK vs eSim Netlist Configuration

**IHP PDK Models:**
- Require `.lib` or `.include` statements to be added manually
- Include highly accurate foundry-level device definitions
- Often contain parameters not supported by default eSim setups

**eSim Netlists:**
- Export basic `.cir` netlists from schematic designs
- Usually do not contain `.control` blocks
- Need simulation directives (`.control`, `.plot`, `.endc`) for execution

This script automates the process of adapting IHP-level detail into the simpler, simulation-ready `.cir` format that eSim/Ngspice understands.

---

### Summary

This automation tool streamlines circuit simulation in eSim by:

- Taking user-defined inputs for simulation type and parameters
- Injecting necessary `.control` blocks into existing `.cir` files
- Automatically including IHP model files where applicable
- Running the simulation using `ngspice` and logging results
