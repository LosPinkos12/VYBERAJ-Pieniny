import os
import shutil

def copy_files_from_camera(source_dir, target_dir):
    # List files in source directory
    try:
        files = os.listdir(source_dir)
    except FileNotFoundError:
        print(f"Source directory '{source_dir}' not found or inaccessible.")
        return

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Copy each file from source to target directory
    for file_name in files:
        source_path = os.path.join(source_dir, file_name)
        dest_path = os.path.join(target_dir, file_name)
        try:
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {file_name}")
        except FileNotFoundError:
            print(f"File '{file_name}' not found or inaccessible.")

def main():
    # Define source and target directories
    source_directory = r"ThisPC\Canon EOS R6\SD1\DCIM\100CANON"
    target_directory = r"C:\Users\YourUsername\Pictures\imported_photos"

    # Copy files from source to target directory
    copy_files_from_camera(source_directory, target_directory)

if __name__ == "__main__":
    main()
