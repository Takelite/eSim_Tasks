# 🧪 Task 3: Simulation Automation Tool

## 🎯 Objective  
The goal of this task was to automate the process of configuring and running simulations in **eSim** using **IHP PDK** models. A Python-based tool was developed that can:

* Take user inputs for simulation type and parameters  
* Automatically generate a valid SPICE circuit file (`.cir`)  
* Optionally run the simulation using `ngspice`  
* Work with or without IHP `.lib` model files

---

## 🔄 Differences Between IHP PDK and eSim

* **Model Format Complexity**  
  IHP PDK model files are rich with advanced parameters designed for professional simulation environments. In contrast, eSim (based on Ngspice) has limited support and may throw errors if unsupported parameters are used.

* **Manual vs. Automated Setup**  
  Setting up simulations manually in eSim involves editing `.cir` files, adding `.lib` references, and writing control statements. This tool automates those steps.

* **Execution Environment**  
  While IHP flows are often GUI-driven, eSim workflows can benefit from CLI automation. This tool fills that gap using Python.

---

## ⚙️ How the Python Script Works

1. **Input Collection**  
   The script prompts the user to provide:
   * Circuit file name (`.cir`)
   * Simulation type (`.tran` or `.dc`)
   * Parameters like time step, stop time, or DC sweep range
   * Optional path to an IHP `.lib` model file

2. **Model Handling**  
   If a `.lib` file is provided, it’s included in the output using `.include`. If not, it checks for `.model` or `.subckt` blocks in the original file.

3. **File Generation**  
   The tool creates a new `.cir` file (e.g., `updated_input.cir`) with:
   * Models included at the top  
   * Original circuit definition  
   * A `.control` block for simulation  
   * Commands to plot output and end the simulation

4. **Simulation (Optional)**  
   If the user chooses, the script runs the simulation using `ngspice` and displays output in the terminal.

---

## 💻 How to Run This Script in VS Code

> These steps assume you already have **Python** and **Ngspice** installed and added to your system PATH.

1. **Open VS Code**  
   Launch Visual Studio Code and open the folder where your script is located.

2. **Place Your Files**  
   * Add your input `.cir` file (e.g., `diode_test.cir`)  
   * Add the model file if needed (e.g., `ihp_diode.lib`)  
   * Make sure the Python script is in the same folder

3. **Open a Terminal in VS Code**  
   Go to the **Terminal** menu → **New Terminal**  
   A terminal window will open at the bottom

4. **Run the Script**  
   In the terminal, run the script using:

   ```bash
   python simulation_tool.py
   ```
## 📝 Provide Inputs

When you run the script, you’ll be prompted to:

- **Enter the circuit file name** (e.g., `diode_test.cir`)
- **Choose simulation type** (`tran` for transient or `dc` for DC analysis)
- **Enter simulation values**:
  - For `tran`: time step and stop time
  - For `dc`: sweep variable, start, stop, and increment
- **Provide the `.lib` model file name**, or just press Enter to skip
- **Confirm if you want to run the simulation**

---

## 📤 Check the Output

- A new `.cir` file will be generated, e.g., `updated_diode_test.cir`
- If you opted to run the simulation, `ngspice` will launch and display the results directly in the terminal

---

## 📌 Summary

- This script makes it easier to run circuit simulations in eSim using IHP models by automatically setting up the simulation files and running them with Ngspice. It saves time, reduces manual errors, and is beginner-friendly.
