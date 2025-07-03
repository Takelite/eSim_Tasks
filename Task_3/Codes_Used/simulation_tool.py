import os
import subprocess

# This function takes all the required inputs from the user
def get_user_inputs():
    print("Simulation Automation Tool for eSim + Ngspice")

    # Ask user for the name of the existing circuit file
    circuit_file = input("Enter existing circuit file name (.cir) exported from eSim: ").strip()

    # Check if the circuit file exists
    if not os.path.exists(circuit_file):
        print(f"Circuit file '{circuit_file}' not found. Please check the name.")
        exit(1)

    # Ask for optional model file path (for IHP PDK)
    ihp_model_path = input("Enter full path to IHP PDK model file (.lib) [Press Enter to skip]: ").strip()
    if ihp_model_path and not os.path.exists(ihp_model_path):
        print(f"IHP model file '{ihp_model_path}' not found. Skipping model include.")
        ihp_model_path = ""

    # Ask user to choose the type of simulation
    simulation_type = input("Enter simulation type (dc / ac / tran): ").strip().lower()

    sim_params = {}

    # Collect simulation parameters based on the type
    if simulation_type == "tran":
        sim_params['tstep'] = input("Time step (e.g., 1n): ").strip()
        sim_params['tstop'] = input("Stop time (e.g., 100n): ").strip()
    elif simulation_type == "dc":
        sim_params['sweep_source'] = input("Sweep source name (e.g., V1): ").strip()
        sim_params['start'] = input("Start value (e.g., 0): ").strip()
        sim_params['stop'] = input("Stop value (e.g., 5): ").strip()
        sim_params['step'] = input("Step size (e.g., 0.1): ").strip()
    elif simulation_type == "ac":
        sim_params['points'] = input("No. of points (e.g., 100): ").strip()
        sim_params['start_freq'] = input("Start frequency (e.g., 1k): ").strip()
        sim_params['stop_freq'] = input("Stop frequency (e.g., 1Meg): ").strip()
    else:
        print("Unsupported simulation type. Use dc, ac, or tran.")
        exit(1)

    # Ask for the nodes the user wants to plot
    plot_command = input("Enter output nodes to plot (e.g., v(out) v(in)): ").strip()

    # Return all inputs as a dictionary
    return {
        "circuit_file": circuit_file,
        "ihp_model_path": ihp_model_path,
        "simulation_type": simulation_type,
        "sim_params": sim_params,
        "plot_command": plot_command
    }


# This function modifies the original .cir file and adds simulation commands
def update_circuit_file(data):
    updated_file = "updated_" + data['circuit_file']

    with open(data['circuit_file'], 'r') as infile, open(updated_file, 'w') as outfile:
        lines = infile.readlines()

        # Write a header comment
        outfile.write("* Updated by Automation Tool\n")

        # Include the IHP model file if provided
        if data['ihp_model_path']:
            outfile.write(f'.include "{data["ihp_model_path"]}"\n')

        # Copy original lines, but skip existing .control blocks
        inside_control = False
        for line in lines:
            if line.strip().lower() == ".control":
                inside_control = True
            if not inside_control:
                outfile.write(line)
            if line.strip().lower() == ".endc":
                inside_control = False

        # Add new .control block with simulation commands
        outfile.write("\n.control\n")
        if data['simulation_type'] == "tran":
            tstep = data['sim_params']['tstep']
            tstop = data['sim_params']['tstop']
            outfile.write(f"tran {tstep} {tstop}\n")
        elif data['simulation_type'] == "dc":
            src = data['sim_params']['sweep_source']
            start = data['sim_params']['start']
            stop = data['sim_params']['stop']
            step = data['sim_params']['step']
            outfile.write(f"dc {src} {start} {stop} {step}\n")
        elif data['simulation_type'] == "ac":
            points = data['sim_params']['points']
            startf = data['sim_params']['start_freq']
            stopf = data['sim_params']['stop_freq']
            outfile.write(f"ac lin {points} {startf} {stopf}\n")

        # Plot the desired output nodes
        outfile.write(f"plot {data['plot_command']}\n")

        # Save simulation results to a .raw file
        outfile.write("write simulation_output.raw\n")
        outfile.write(".endc\n")
        outfile.write(".end\n")

    print(f"\nUpdated circuit file created: {updated_file}")
    return updated_file


# This function runs the simulation using Ngspice on the updated .cir file
def run_simulation(cir_file):
    print("\nRunning simulation using Ngspice...")

    # Run Ngspice and capture output
    result = subprocess.run(["ngspice", cir_file], capture_output=True, text=True)

    # Save simulation logs
    with open("simulation_log.txt", "w") as log_file:
        log_file.write(result.stdout)
        log_file.write(result.stderr)

    # Show status message
    if result.returncode == 0:
        print("Simulation completed. Log saved to simulation_log.txt")
    else:
        print("Simulation failed. Check simulation_log.txt for details.")


# Main function to organize execution
def main():
    print("eSim Simulation Automation Tool with IHP PDK Support")
    data = get_user_inputs()                 # Step 1: Get user input
    updated_cir = update_circuit_file(data)  # Step 2: Modify circuit file
    run_simulation(updated_cir)              # Step 3: Run Ngspice simulation


# Entry point for the script
if __name__ == "__main__":
    main()
