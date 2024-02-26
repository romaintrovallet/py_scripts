import subprocess
import os

global CUR_PATH
global OUT_PATH
global CONF_PATH

def init():
    global CUR_PATH, OUT_PATH, CONF_PATH
    CUR_PATH = os.getcwd()
    OUT_PATH = os.path.join(CUR_PATH, "py_scripts\git-free\out")
    CONF_PATH = os.path.join(CUR_PATH, "py_scripts\git-free\config")


def read_file(name, selector, type):
    if type == "out":
        file_path = os.path.join(OUT_PATH, name + ".txt")
    elif type == "conf":
        file_path = os.path.join(CONF_PATH, name + ".txt")
    else:
        print("type is badly set, can only get value 'out' or 'conf'")
        return

    if os.path.isfile(file_path):  
        print ("file is valid")  
        # Initialize an empty list to store the relevant lines
        lines = []        
        
        # Read the input file line by line
        with open(file_path, "r") as input_file:
            for line in input_file:
                if line.strip().startswith(selector):
                    if type == "conf":
                        ret = line.split("=")[1]
                        return ret.rstrip('\n')
                    else :   
                        lines.append(line)                    
        return lines
    else:
        print(f"file not valid for {file_path}")
        return 0 


def save_file(content, name):
    file_path = os.path.join(OUT_PATH, name)
    with open(file_path, "w") as output_file:
        output_file.write(content)
        print(f"Output saved to '{file_path}'")


def run_cmd(cmd, name=None, directory=None, save_error=None):
    list = cmd.split()
    try:
        # Execute the command
        if directory:
            result = subprocess.run(list, capture_output=True, text=True, check=True, cwd=directory)
        else:
            result = subprocess.run(list, capture_output=True, text=True, check=True)

        # Print the output to the console
        print("Command output:")
        print(result.stdout)

        # Save the output to a file
        if name and result.stdout:
            filename = name + "_out.txt"
            save_file(result.stdout, filename)
        
        return 1

    except subprocess.CalledProcessError as e:
        print(f"Error executing {name}: {e.stderr}")
        if name and save_error:
            # Save the output to a file
            filename = os.path.join(name + "_out.txt")
            save_file(e.stderr, filename)
        return 0


def run_cmd1():
    cmd = read_file("cmd_test", "cmd_1", "conf")
    name = cmd.split()[0]

    run_cmd(cmd, name=name)

def run_cmd2():
    cmd = read_file("cmd_test", "cmd_2", "conf")
    name = cmd.replace(" ","_")
    search = cmd.split()[0]

    directory = read_file("cmd_test", search +"_path","conf")
    if os.path.isdir(directory):  
        print ("directory is valid")
        return run_cmd(cmd, name=name, directory=directory, save_error=True)
    else:
        print("directory not valid")
        return 1

def run_cmd3():
    cmd = read_file("cmd_test", "cmd_2", "conf")
    name = cmd.replace(" ","_")
    search = read_file("cmd_test", "cmd_3", "conf")

    file = name + "_out"
    lines = read_file(file, search, "out")      
    if lines :    
        for line in lines:
            run_cmd(line)


if __name__ == "__main__":
    init()
    run_cmd1()
    if not run_cmd2():
        run_cmd3()
