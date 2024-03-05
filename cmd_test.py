import subprocess
import os
import time
import sys
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

def create_command(app, ret_type=None):
    # Name
    app_name = t.read_file("cmd_test", app, "conf")
    # Path
    selector_path = app_name.replace(" ","_") + "_path"
    app_path = t.read_file("cmd_test", selector_path, "conf")
    app_exe = os.path.basename(app_path)
    # Args
    args = []
    selector_args = app_name.replace(" ","_") + "_args"
    string_args = t.read_file("cmd_test", selector_args, "conf").split(" ")
    for arg in string_args:
        args.append(arg)

    if ret_type == "cmd":
        return [app_path, *args]
    else:
        return [app_path, *args], app_exe, app_name

def open_app(app):
    command, app_exe, app_name = create_command(app)
    try:        
        # Launch App
        process = subprocess.Popen(command, shell=True)
        print(f"{app_name} opened successfully!")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        process = None
    return process, app_exe


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

def open_app1():
    # Opens app_1
    process_1, app_exe_1 = open_app("app_1")
    print(process_1)
    time.sleep(10)
    subprocess.Popen(["taskkill", "/F", "/IM", app_exe_1])
    time.sleep(10)
    process_1, app_exe_1 = open_app("app_1")
    time.sleep(10)
    subprocess.Popen(["taskkill", "/F", "/IM", app_exe_1])

def open_app2():
    command = create_command("app_1", ret_type="cmd")
    print(command)
    # Start the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Read and display the output in real time
    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()

        if stdout_line:
            sys.stdout.write(stdout_line)
        if stderr_line:
            sys.stderr.write(stderr_line)

        # Check if the process has completed
        if process.poll() is not None:
            break


if __name__ == "__main__":
    t.init()
    # run_cmd1()
    # if not run_cmd2():
    #     run_cmd3()
    # open_app1()
    open_app2()
