import os
import filecmp
import difflib
import toolbox as t


global folders_to_ignore

def init():
    global folders_to_ignore
    folders_to_ignore = []
    list = t.read_file("compare_folders", "folder_to_ignore","conf")
    folders = list.split(',')
    for folder in folders:
        folders_to_ignore.append(folder)
    print(folders_to_ignore)


def compare_folders(folder1, folder2, ignore_folders=None):
    if ignore_folders == None:
        ignore_folders = [];

    diffs = []
    for root, dirs, files in os.walk(folder1):
        relative_path = os.path.relpath(root, folder1)
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        for file in files:
            file_path1 = os.path.join(root, file)
            file_path2 = os.path.join(folder2, relative_path, file)
            if not os.path.exists(file_path2):
                diffs.append((file_path1, "File not found in second directory"))
            elif not filecmp.cmp(file_path1, file_path2, shallow=False):
                with open(file_path1, 'r', encoding='utf-8') as f1, open(file_path2, 'r', encoding='utf-8') as f2:
                    try:
                        diff = difflib.unified_diff(f1.readlines(), f2.readlines(), lineterm='')
                    except Exception as e:
                        print(f"Error {e} in diff_lib comparing {f1} and {f2}")
                    diff_str = '\n'.join(diff)
                    diffs.append((file_path1, "Files are different", diff_str))
    
    for root, dirs, files in os.walk(folder2):
        relative_path = os.path.relpath(root, folder2)
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        for file in files:
            file_path1 = os.path.join(root, file)
            file_path2 = os.path.join(folder1, relative_path, file)
            if not os.path.exists(file_path2):
                diffs.append((file_path1, "File not found in first directory"))
    
    return diffs

t.init()
init()
# Example usage
dir1_path = t.read_file("compare_folders", "dir1", "conf")
dir2_path = t.read_file("compare_folders", "dir2", "conf")

diffs = compare_folders(dir1_path, dir2_path, folders_to_ignore)

for diff in diffs:
    print("File:", diff[0])
    print("--------------")
    print("Difference Type:", diff[1])
    if len(diff) > 2:
        print("Differences:")
        print(diff[2])
    elif len(diff) < 2:
        print(diff) 
    print("=========")
print("="*50)