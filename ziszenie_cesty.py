import os
import win32com.client

def is_camera_connected():
    wmi = win32com.client.GetObject("winmgmts:")
    cameras = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Caption LIKE '%Canon EOS R6%'")

    # Ak existuje aspoň jedno zariadenie Canon EOS R6, považujeme kameru za pripojenú
    return len(cameras) > 0

def list_files_from_camera():
    file_list = []
    wmi = win32com.client.GetObject("winmgmts:")

    # Získanie všetkých zariadení, vrátane pripojených k fotoaparátu Canon EOS R6
    devices = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Caption LIKE '%Canon EOS R6%'")
    
    for device in devices:
        device_id = device.DeviceID
        path = f"\\\\.\\{device_id}\\ROOT\\Image"

        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    file_list.append(dir_path)
        except Exception as e:
            print(f"Chyba pri prehľadávaní zariadenia: {str(e)}")

    return file_list, device_id if devices else None

def main():
    if is_camera_connected():
        files, device_id = list_files_from_camera()
        if len(files) > 0:
            print("Nájdené súbory a priecinky na fotoaparáte Canon EOS R6:")
            for file in files:
                print(file)
        else:
            print(f"Na zariadení s ID '{device_id}' nie sú žiadne súbory alebo priecinky.")
    else:
        print("Fotoaparát Canon EOS R6 nie je pripojený.")

    input("Stlačte Enter pre ukončenie skriptu...")

if __name__ == "__main__":
    main()
