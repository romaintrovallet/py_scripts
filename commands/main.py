import os
from os import path as p
import sys

pyscripts_path = p.dirname(p.dirname(p.realpath(__file__)))
sys.path.append(pyscripts_path)
import toolbox as t
import security as s

def execute_json_command(infos):
    path = os.path.expanduser(infos[0].get("path"))
    cmd = infos[0].get("cmd")
    security_flag = True
    if len(infos[0]) > 2:
        print(infos[0])
        print(f"len infos = {len(infos[0])}")
        security = infos[0].get("security")
        security_flag = s.execute_security(security)
    if os.path.isdir(path) and security_flag:
        os.chdir(path)
        os.system(f'start cmd /k ; {cmd}')
    else:
        if not os.path.isdir(path):
            print(f"\n Error : Could not open console as {path} is not a real dir\n")
        if not security_flag:
            print(f"\n Error : Security did not pass : security_flag={security_flag}\n")

def retrieve_json_infos(letter):
    infos = []
    retrieved_infos = t.read_conf_json_file("commands", letter)
    infos.append(retrieved_infos)
    return infos

def retrieve_json_and_execute(letter):
    print(f"\n\n -- Execution of command {letter} --")
    infos = retrieve_json_infos(letter)
    execute_json_command(infos)

t.init()

retrieve_json_and_execute("A")
retrieve_json_and_execute("B")
