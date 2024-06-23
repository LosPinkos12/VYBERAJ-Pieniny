
import subprocess
import time
import os
import shutil
import win32com.client

def is_camera_connected():
    wmi = win32com.client.GetObject("winmgmts:")
    cameras = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Caption LIKE '%Canon EOS R6%'")

    # Ak existuje aspoň jedno zariadenie Canon EOS R6, považujeme kameru za pripojenú
    return len(cameras) > 0

def list_files():
    # Simulácia získania zoznamu súborov
    return ["#1 IMG_0001.CR2", "#2 IMG_0002.CR2", "#3 IMG_0003.CR2"]

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

            # Download the file (simulating with copying for example)
            src_path = os.path.join('source_directory', file_name)
            dest_path = os.path.join(target_dir, file_name)
            shutil.copy(src_path, dest_path)
            print(f'Stiahnuté {file_name}')
            
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
    try:
        main()
    except Exception as e:
        print(f"Nastala chyba: {str(e)}")
    
    # Pauza na konci, aby ste si stihli prečítať chybové hlásenie
    input("Stlačte Enter pre ukončenie programu...")