import os
import json

global CUR_PATH
global OUT_PATH
global CONF_PATH

def init(uproot=0):
    global CUR_PATH, OUT_PATH, CONF_PATH
    CUR_PATH = os.getcwd()
    if uproot:
        for _ in range(uproot):
            CUR_PATH = os.path.dirname(CUR_PATH)
    git_path = os.path.join(CUR_PATH, "py_scripts")
    if os.path.isdir(git_path):
        OUT_PATH = os.path.join(git_path, "git-free\out")
        CONF_PATH = os.path.join(git_path, "git-free\config")
        return True
    else:
        print(f"Path given is not valid : {git_path}")
        print("Git is badly setup or use uproot")
        return False


def get_file(name, type, ext):
    if type == "out":
        file_path = os.path.join(OUT_PATH, name + ext)
    elif type == "conf":
        file_path = os.path.join(CONF_PATH, name + ext)
    else:
        print(f"Got type = {type} and should either be 'out' or 'conf'")
        return 0
    
    if os.path.isfile(file_path):  
        print(f"{file_path} is valid")
        return file_path
    else:
        return 0    

def open_txt(selector, file_path):
    lines = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            if selector :
                if line.strip().startswith(selector):
                    if type == "conf":
                        ret = line.split("{")[1]
                        return ret.rstrip('\n').rstrip('}')
                    else :
                        lines.append(line)
            else :
                lines.append(line)
    return lines

def open_json(selector, file_path):
    with open(file_path, "r") as input_file:
        data = json.load(input_file)
        return data.get(selector)

def read_file(name, selector, type, ext=".txt"):
    file_path = get_file(name, type, ext)
    if file_path:
        lines = []
        # Read the input file line by line
        if ext == ".txt":
            lines = open_txt(selector, file_path)
        elif ext == ".json":
            lines = open_json(selector, file_path)
        return lines
    else:
        print(f"file not valid for {file_path}")
        return 0

def read_conf_file(name, selector):
    return read_file(name, selector, "conf")

def read_conf_json_file(name, selector):
    return read_file(name, selector, "conf", ext=".json")

def save_file(content, name):
    file_path = os.path.join(OUT_PATH, name)
    with open(file_path, "w") as output_file:
        output_file.write(content)
        print(f"Output saved to '{file_path}'")
