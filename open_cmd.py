import os
import sys
import toolbox as t

def get_download_path():
    # Get the user's home directory (e.g., C:\Users\Username)
    home_directory = os.path.expanduser("~")
    # Define the path to the Download directory
    download_directory = os.path.join(home_directory, "Downloads")
    return download_directory

def open_command_prompt_at_download_directory():
    download_directory = get_download_path()
    
    try:
        os.chdir(download_directory)
        os.system("start cmd")
        print(f"Command prompt opened at {download_directory}")
    except FileNotFoundError:
        print(f"Error: The specified directory '{download_directory}' does not exist.")

def create_hello_world_program():
    download_directory = get_download_path()

    # Create a subdirectory within Downloads
    new_directory = os.path.join(download_directory, "my_hello_world")
    os.makedirs(new_directory, exist_ok=True)

    # Change the working directory to the new subdirectory
    os.chdir(new_directory)

    # Create a main.c file with a simple "Hello, world!" program
    with open("main.c", "w") as f:
        f.write("#include <stdio.h>\n\nint main() {\n")
        f.write("    printf(\"Hello, world!\\n\");\n")
        f.write("    return 0;\n}\n")

    print(f"Created 'main.c' in '{new_directory}'")

def open_venv():
    venv_path = t.read_file("open_cmd", "venv_path", "conf")
    # Path to the virtual environment's activation script
    activate_script = os.path.join(venv_path, "Scripts", "activate")

    # Print the path to the Python interpreter
    print(f"We are using Python outside of venv")
    print(f"Interpreter path: {sys.executable}")

    # Execute the activation script
    os.system(f"{activate_script}")

    # Print the path to the Python interpreter
    print(f"We are using Python from the virtual environment:")
    print(f"Interpreter path: {sys.executable}")

    os.system("deactivate")

    # Print the path to the Python interpreter
    print(f"We are using Python outside of venv")
    print(f"Interpreter path: {sys.executable}")

if __name__ == "__main__":
    t.init()
    open_command_prompt_at_download_directory()
    create_hello_world_program()
    # open_venv()