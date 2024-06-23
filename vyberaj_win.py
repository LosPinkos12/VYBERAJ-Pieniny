import os
import time
import shutil
import win32file
import win32con

# Adresár, kam sa majú kopírovať fotky
destination_folder = r"C:\path\to\your\folder"

def is_camera_connected():
    try:
        # Získanie zoznamu pripojených zariadení USB
        drives = win32file.GetLogicalDrives()
        for i in range(1, 26):
            if drives & (1 << i):
                drive_letter = chr(65 + i) + ':\\'
                drive_type = win32file.GetDriveType(drive_letter)
                if drive_type == win32file.DRIVE_REMOVABLE:
                    volume_info = win32file.GetVolumeInformation(drive_letter)
                    if "Canon" in volume_info[0]:
                        return drive_letter
        return None
    except Exception as e:
        print(f"Chyba pri kontrole pripojených zariadení: {e}")
        return None

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

def download_photos(drive_letter, existing_files, imported_files):
    source_dir = f"{drive_letter}\\DCIM\\100CANON"  # Príklad cesty, môžete upraviť podľa potreby
    target_dir = 'stiahnute_fotky'
    os.makedirs(target_dir, exist_ok=True)

    try:
        for filename in os.listdir(source_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) and filename not in imported_files:
                shutil.copy(os.path.join(source_dir, filename), os.path.join(target_dir, filename))
                print(f'Presunuté do: {os.path.join(target_dir, filename)}')
                imported_files.append(filename)

        return len(imported_files)
    
    except Exception as e:
        print(f"Chyba pri kopírovaní fotiek: {e}")
        return 0

def main():
    target_dir = 'stiahnute_fotky'
    imported_files_file = 'importovane_fotky.txt'
    imported_files = load_imported_files(imported_files_file)

    while True:
        drive_letter = is_camera_connected()
        if drive_letter:
            user_input = input("Kamera je pripojená. Stlač (enter) pre import fotiek alebo 'q' pre ukončenie: ").strip().lower()
            if user_input == '':
                imported_count = download_photos(drive_letter, target_dir, imported_files)
                print(f'Importovalo {imported_count} nových fotiek.')
                save_imported_files(imported_files_file, imported_files)
            elif user_input == 'q':
                break
        else:
            print("Kamera nie je pripojená.")
        
        time.sleep(5)

if __name__ == '__main__':
    main()
