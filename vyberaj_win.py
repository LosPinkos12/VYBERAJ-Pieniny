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

def list_files(source_dir):
    # Zoznam všetkých súborov v adresári source_dir
    files = os.listdir(source_dir)
    return files

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
    # Pre jednoduchosť pri prechádzaní zoznamu súborov sa táto funkcia môže preskočiť

    # Vrátime 0, pretože všetky súbory budeme pokladať za nové
    return 0

def download_photos(existing_files, imported_files, source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    files_to_copy = list_files(source_dir)
    imported_count = 0

    start_time = time.time()  # Record the start time

    for file_name in files_to_copy:
        if file_name not in existing_files and file_name not in imported_files:
            # Check if camera is still connected
            if not is_camera_connected():
                print("Kamera nie je pripojená. Ukončenie importu.")
                return imported_count

            # Construct full source and destination paths
            src_path = os.path.join(source_dir, file_name)
            dest_path = os.path.join(target_dir, file_name)

            try:
                # Copy the file
                shutil.copy(src_path, dest_path)
                print(f'Skopiovaný súbor: {file_name}')

                imported_files.append(file_name)
                imported_count += 1
            except Exception as e:
                print(f'Chyba pri kopírovaní súboru {file_name}: {str(e)}')

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time  # Calculate the total time taken
    print(f'Celkový čas importu: {total_time:.2f} sekúnd')

    return imported_count

def main():
    source_dir = 'source_directory'
    target_dir = 'stiahnute_fotky'
    imported_files_file = 'importovane_fotky.txt'
    
    existing_files = get_existing_files(target_dir)
    imported_files = load_imported_files(imported_files_file)

    while True:
        if is_camera_connected():
            # Skopírovať všetky súbory z source_dir, ktoré ešte neboli importované
            imported_count = download_photos(existing_files, imported_files, source_dir, target_dir)
            print(f'Importovalo {imported_count} nových fotiek.')

            # Uložiť importované súbory do súboru
            save_imported_files(imported_files_file, imported_files)
        else:
            print("Kamera nie je pripojená.")
        
        # Čakať 1 sekundu pred ďalším cyklom
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Nastala chyba: {str(e)}")
    
    # Pauza na konci, aby ste si stihli prečítať chybové hlásenie
    input("Stlačte Enter pre ukončenie programu...")
