import filecmp
import os.path

folder_to_ignore = ['folder1', 'folder2']

def check_directory_exists(directory_path):
    """
    Checks if the specified directory path exists.

    :param directory_path: Path to the directory
    :return: True if the directory exists, False otherwise
    """
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

def compare_directories(dir1, dir2):
    """
    Compare two directories recursively and display differences.
    
    @param dir1: First directory path
    @param dir2: Second directory path
    """

    if not check_directory_exists(dir1):
        if not check_directory_exists(dir2):
            print("Error: both directories do not exist.")
        print("Error: Only dir 1 does not exist.")
        return
    if not check_directory_exists(dir2):
        print("Error: Only dir 2 does not exist.")
        return
    
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    
    # Compare files within common directories
    _, mismatch, errors = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    
    if mismatch:
        print("Files with differences:")
        for filename in mismatch:
            print(f"- {filename}")
    
    if errors:
        print("Error comparing files:")
        for filename in errors:
            print(f"- {filename}")
    
    # Recursively compare subdirectories
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        compare_directories(new_dir1, new_dir2)

def compare_directories_detailed(dir1, dir2, parent_path=""):
    """
    Compare two directories recursively and display detailed differences.

    :param dir1: First directory path
    :param dir2: Second directory path
    :param parent_path: Parent path for displaying file paths
    """
    if not check_directory_exists(dir1) or not check_directory_exists(dir2):
        print("Error: One or both directories do not exist.")
        return

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    
    # Compare files within common directories
    _, mismatch, errors = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    
    if mismatch:
        print(f"Files with differences in {parent_path}:")
        for filename in mismatch:
            print(f"- {os.path.join(parent_path, filename)}")
    
    if errors:
        print(f"Error comparing files in {parent_path}:")
        for filename in errors:
            print(f"- {os.path.join(parent_path, filename)}")
    
    # Recursively compare subdirectories
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        compare_directories_detailed(new_dir1, new_dir2, os.path.join(parent_path, common_dir))

# Example usage
dir1_path = r"<path>\<to>\<folder>\<one>"
dir2_path = r"<path>\<to>\<folder>\<two>"

compare_directories_detailed(dir1_path, dir2_path)
