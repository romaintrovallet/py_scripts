import subprocess
import os
import toolbox as t

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
            t.save_file(result.stdout, filename)
        
        return 1

    except subprocess.CalledProcessError as e:
        print(f"Error executing {name}: {e.stderr}")
        if name and save_error:
            # Save the output to a file
            filename = os.path.join(name + "_out.txt")
            t.save_file(e.stderr, filename)
        return 0


def run_cmd1():
    cmd = t.read_file("cmd_test", "cmd_1", "conf")
    name = cmd.split()[0]

    run_cmd(cmd, name=name)

def run_cmd2():
    cmd = t.read_file("cmd_test", "cmd_2", "conf")
    name = cmd.replace(" ","_")
    search = cmd.split()[0]

    directory = t.read_file("cmd_test", search +"_path","conf")
    if os.path.isdir(directory):  
        print ("directory is valid")
        return run_cmd(cmd, name=name, directory=directory, save_error=True)
    else:
        print(f"directory not valid for {directory}")
        return 1

def run_cmd3():
    cmd = t.read_file("cmd_test", "cmd_2", "conf")
    name = cmd.replace(" ","_")
    search = t.read_file("cmd_test", "cmd_3", "conf")

    file = name + "_out"
    lines = t.read_file(file, search, "out")      
    if lines :    
        for line in lines:
            run_cmd(line)


if __name__ == "__main__":
    t.init()
    run_cmd1()
    if not run_cmd2():
        run_cmd3()
