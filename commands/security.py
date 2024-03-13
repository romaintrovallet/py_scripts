import os
from os import path as p
import subprocess
import sys

pyscripts_path = p.dirname(p.dirname(p.realpath(__file__)))
sys.path.append(pyscripts_path)
import toolbox as t

DEBUG = False

def check_results(saved_results, waited_results):
    flag = False
    for waited_result in waited_results:
        flag = False
        for saved_result in saved_results:
            if waited_result in saved_result:
                flag = True
                break
            elif DEBUG:
                print(f"Could not find waited result {waited_result} in saved result {saved_result}")
    return flag


def execute_security(security):
    # Config
    path = security.get("path")
    cmd = security.get("cmd")
    waited_result = security.get("result").split()
    ack_run = 0
    naming="security"
    
    # Execute command
    if path:
        ack_run = run_cmd(cmd, directory=path, name=naming)
    else :
        ack_run = run_cmd(cmd, name=naming)

    # Check results
    if ack_run:
        saved_result_path = os.path.join(t.OUT_PATH, f"{naming}_out.txt")
        saved_result = t.open_txt(False, saved_result_path)
        if check_results(saved_result, waited_result):
            return True
        else:
            print("Error occured after the check of the saved result")
            print(f"Parameters : path = {path} / cmd = {cmd}")
            print(f"Results : waited = {waited_result} / saved = {saved_result}")
            return False
    else:
        print("Error occured after the command execution")
        print(f"Parameters : path = {path} / cmd = {cmd}")
        return False

def run_cmd(cmd, name=False, directory=False, save_error=False):
    list = cmd.split()
    print(list)
    try:
        # Execute the command
        if directory:
            result = subprocess.run(list, capture_output=True, text=True, check=True, cwd=directory)
        else:
            result = subprocess.run(list, capture_output=True, text=True, check=True)

        if result.stdout:
            # print("Command output:")
            # print(result.stdout)
            if name:
                filename = name + "_out.txt"
                t.save_file(result.stdout, filename)
        if result.stderr:
            # print("Command error:")
            # print(result.stderr)
            if save_error and name:
                filename = name + "_out.txt"
                t.save_file(result.stderr, filename)
        return 1

    except subprocess.CalledProcessError as e:
        print(f"Error executing {name}: {e.stderr}")
        if name and save_error:
            # Save the output to a file
            filename = os.path.join(name + "_out.txt")
            t.save_file(e.stderr, filename)
        return 0
