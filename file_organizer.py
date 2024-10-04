import os
import shutil
import sys
import json

folder_mappings = {
    'Images': ['.png', '.jpg'],
    'Documents': ['.pdf', '.docx', '.zip'],
    'Software': ['.exe'],
    'Audio': ['.mp3', '.mp4']
}

def create_dirs(base_path):
   
    for folder in folder_mappings.keys():
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created directory: {folder_path}")

def copy_files(source_path):

    json_paths = {folder: set() for folder in folder_mappings.keys()}

    for root, _, files in os.walk(source_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            for folder, extensions in folder_mappings.items():
                if file_ext in extensions:
                    dest_folder = os.path.join(source_path, folder)
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_folder, file)

                  
                    if not os.path.exists(dest_file):
                        shutil.copy2(src_file, dest_file)  
                        json_paths[folder].add(dest_file) 
                    break

    # Create a JSON file for each folder
    for folder, paths in json_paths.items():
        json_file_path = os.path.join(source_path, folder, f"{folder}_files.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(list(paths), json_file, indent=4)  
        print(f"Created JSON file: {json_file_path}")

def main(source):
    source_path = os.path.abspath(source)

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source directory '{source_path}' does not exist.")

    create_dirs(source_path)
    copy_files(source_path)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("You must pass a source directory.")

    source = args[1]
    main(source)
