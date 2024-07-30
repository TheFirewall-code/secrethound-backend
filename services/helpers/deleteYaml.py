import os
from datetime import datetime
import glob

def delete_old_files():
    # Folder path where YAML files are stored
    folder_path = "pr_scan"

    # Maximum number of YAML files allowed
    max_files = 300
    yaml_files = glob.glob(os.path.join(folder_path, '*.yaml'))
    if len(yaml_files) <= max_files:
        print("No action needed. Total YAML files are within the limit.")
        return True

    # Sort files by creation date
    yaml_files.sort(key=lambda x: os.path.getctime(x))

    # Calculate how many files to delete
    files_to_delete = len(yaml_files) - max_files

    # Delete the oldest files
    for i in range(files_to_delete):
        os.remove(yaml_files[i])
        print(f"Deleted: {yaml_files[i]}")

    print(f"Total YAML files after deletion: {max_files}")

    return True

'''
# Folder path where YAML files are stored
folder_path = "pr_scan"

# Maximum number of YAML files allowed
max_files = 300

delete_old_files(folder_path, max_files)
'''