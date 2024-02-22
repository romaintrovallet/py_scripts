import subprocess

def run_nrfjprog():
    try:
        # Execute the nrfjprog command
        result = subprocess.run(["nrfjprog", "--com"], capture_output=True, text=True, check=True)

        # Print the output to the console
        print("Command output:")
        print(result.stdout)

        # Save the output to a file
        with open("nrfjprog_output.txt", "w") as output_file:
            output_file.write(result.stdout)
            print(f"Output saved to 'nrfjprog_output.txt'")

    except subprocess.CalledProcessError as e:
        print(f"Error executing nrfjprog: {e.stderr}")

if __name__ == "__main__":
    run_nrfjprog()
