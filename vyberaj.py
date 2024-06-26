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

def get_existing_files(target_dir):
    if not os.path.exists(target_dir):
        return []
    return os.listdir(target_dir)

def load_imported_files(file_path):
    imported_files = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            imported_files = file.read().splitlines()
    return imported_files

def save_imported_files(file_path, imported_files):
    with open(file_path, 'w') as file:
        for file_name in imported_files:
            file.write(file_name + '\n')

def count_new_photos(existing_files, imported_files):
    file_lines = list_files()
    new_photos_count = 0

    for file_info in file_lines:
        parts = file_info.split()
        file_name = parts[-1]

        if file_name not in existing_files and file_name not in imported_files:
            new_photos_count += 1

    return new_photos_count

def download_photos(existing_files, imported_files):
    target_dir = 'stiahnute_fotky'
    os.makedirs(target_dir, exist_ok=True)

    file_lines = list_files()
    imported_count = 0

    start_time = time.time()  # Record the start time

    for file_info in file_lines:
        parts = file_info.split()
        file_number = parts[0][1:]  # Remove the leading '#'
        file_name = parts[-1]

        if file_name not in existing_files and file_name not in imported_files:
            # Check if camera is still connected
            if not is_camera_connected():
                print("Kamera nie je pripojená. Ukončenie importu.")
                return imported_count

            # Download the file
            download_cmd = ['gphoto2', '--get-file', file_number, '--filename', os.path.join(target_dir, file_name)]
            subprocess.run(download_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            #print(f'Stiahnuté {file_name}')
            
            # Rename and move the file
            new_file_name = f"{os.path.splitext(file_name)[0]}.jpg"  # Add .jpg extension
            new_file_path = os.path.join(target_dir, new_file_name)
            os.rename(os.path.join(target_dir, file_name), new_file_path)
            print(f'Presunuté do: {new_file_path}')

            imported_files.append(file_name)
            imported_count += 1

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time  # Calculate the total time taken
    print(f'Celkový čas importu: {total_time:.2f} sekúnd')

    return imported_count

def main():
    target_dir = 'stiahnute_fotky'
    imported_files_file = 'importovane_fotky.txt'
    existing_files = get_existing_files(target_dir)
    imported_files = load_imported_files(imported_files_file)

    while True:
        if is_camera_connected():
            # Count new photos before asking for import
            new_photos_count = count_new_photos(existing_files, imported_files)
            if new_photos_count == 0:
                print("Dostupných 0 nových fotiek na import.")
            else:
                print("Kamera je pripojená.")
                print(f"Dostupných {new_photos_count} nových fotiek na import.")

                user_input = input("Stlač (enter) pre import fotiek.").strip().lower()
                print()
                if user_input == '':
                    imported_count = download_photos(existing_files, imported_files)
                    print(f'Importovalo {imported_count} nových fotiek, LAČES.')
                    print()

                    # Save imported files to file
                    save_imported_files(imported_files_file, imported_files)
                else:
                    print("Neimportovalo žiadne fotky.")
        else:
            print("Kamera nie je pripojená.")
        
        time.sleep(1)  # Delay to prevent rapid looping and to give time for user action

if __name__ == '__main__':
    main()
