import subprocess
import time
import os

def is_camera_connected():
    result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True)
    return "Canon" in result.stdout

def list_files():
    result = subprocess.run(['gphoto2', '--list-files'], capture_output=True, text=True)
    files = result.stdout.splitlines()
    file_lines = [line for line in files if line.startswith('#')]
    return file_lines

def download_photos():
    target_dir = 'downloaded_photos'
    os.makedirs(target_dir, exist_ok=True)

    file_lines = list_files()

    for file_info in file_lines:
        parts = file_info.split()
        file_number = parts[0][1:]  # Remove the leading '#'
        file_name = parts[-1]
        
        # Download the file
        download_cmd = ['gphoto2', '--get-file', file_number, '--filename', os.path.join(target_dir, file_name)]
        subprocess.run(download_cmd)
        print(f'Downloaded {file_name}')
        
        # Rename and move the file
        new_file_name = f"{os.path.splitext(file_name)[0]}.jpg"  # Add .jpg extension
        new_file_path = os.path.join(target_dir, new_file_name)
        os.rename(os.path.join(target_dir, file_name), new_file_path)
        print(f'Renamed and moved to {new_file_path}')

def main():
    print("Starting camera monitor...")

    while True:
        if is_camera_connected():
            print("Camera is connected.")
            user_input = input("Do you want to import photos? (yes/no): ").strip().lower()
            if user_input == 'yes':
                download_photos()
        else:
            print("Camera is not connected.")
        
        time.sleep(1)  # Check every 1 second

if __name__ == '__main__':
    main()
