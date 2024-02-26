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
