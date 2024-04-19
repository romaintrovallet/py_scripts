import os
import shutil

def find_folders(path, target_folder):
    found_folders = []
    # Get immediate subfolders
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    # Check if pattern
    for subfolder in subfolders:
        folder_name = os.path.basename(subfolder)
        # Found a folder
        if folder_name == target_folder or folder_name.startswith(target_folder):
            found_folders.append(subfolder)
        # if does not correspond call recursively
        else:
            found_folders.extend(find_folders(subfolder, target_folder))
    return found_folders

def keep_selected(folder, filename):
    files = os.listdir(folder)    

    for file in files:
        file_path = os.path.join(folder, file)
        if file.lower() != filename.lower():
            # Deletion
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Folder {file} is deleted.")
                elif os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File {file} is deleted.")
                else:
                    print(f"{file} not recognize as a file or a folder.")
            except OSError as e:
                print(f"Error when deleting files : {e.strerror}\n")
        # Preservation
        else:
            print(f"File {file} is PRESERVED.")

def verify_presence(name, target):
    return os.path.exists(os.path.join(name, target))

def keep_file(path, file_to_keep):
    print(f"\nPath = {path}")
    if os.path.exists(os.path.join(path, "zephyr")):
        # Ask if delete
        ret = input("Do you want to remove unnecessay content from this folder (y/n):")
        # Delete
        if ret == "y" or ret == "yes":
            keep_selected(path, file_to_keep)
    else:
        print("Already deleted\n")

def find_targets(path, target):
    flag = True
    found_targets = []
    # Get immediate layer
    contents = [f.path for f in os.scandir(path)]
    for content in contents:
        content_name = os.path.basename(content)
        # Found a content
        if content_name == target:
            found_targets.append(content)
            flag = False
        # if does not correspond call recursively
    for content in contents:
        if os.path.isdir(content) and flag:
            found_targets.extend(find_targets(content, target))
    return found_targets

folder_path = r'C:\ncs\apps'
folder_pattern = "build"
file_to_keep = 'CMakeCache.txt'

patterns_path = find_folders(folder_path, folder_pattern)

for folder in patterns_path:
    print("\n==================")
    print(f"Folder = {folder}")
    targets_path = find_targets(folder, file_to_keep)
    for target in targets_path:
        keep_file(os.path.dirname(target), file_to_keep)
        
    print("------------------")
