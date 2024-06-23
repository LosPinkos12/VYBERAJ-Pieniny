import os
import shutil
import time
import win32file
import win32api
import win32con
import threading

# Adresár, kam sa majú kopírovať fotky
destination_folder = r"C:\\k\priecinku"

def copy_photos(source_dir, dest_dir):
    print("Copying photos from", source_dir, "to", dest_dir)
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            shutil.copy(os.path.join(source_dir, filename), dest_dir)
            print("Copied", filename)

def monitor_usb():
    device_filter = win32file.HDEVINFO()
    win32file.SetupDiGetClassDevs(None, 'USB', None, win32file.DIGCF_PRESENT | win32file.DIGCF_DEVICEINTERFACE)
    while True:
        win32file.SetupDiEnumDeviceInterfaces(device_filter, None, 'USB', None)
        time.sleep(1)

def device_event(device):
    if 'Canon' in device:
        print("Canon EOS R6 detected.")
        source_dir = device
        copy_photos(source_dir, destination_folder)

def main():
    monitoring_thread = threading.Thread(target=monitor_usb)
    monitoring_thread.start()
    print("Monitoring for Canon EOS R6 connections...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitoring_thread.join()

if __name__ == "__main__":
    main()
