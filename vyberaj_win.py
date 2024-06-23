import os
import shutil
import time
import threading
import pywinusb.hid as hid

# Adresár, kam sa majú kopírovať fotky
destination_folder = r"C:\cesta\k\priecinku"

def copy_photos(source_dir, dest_dir):
    print("Copying photos from", source_dir, "to", dest_dir)
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            shutil.copy(os.path.join(source_dir, filename), dest_dir)
            print("Copied", filename)

def monitor_usb():
    # Funkcia na monitorovanie USB zariadení pomocou pywinusb
    devices = hid.find_all_hid_devices()

    while True:
        for device in devices:
            if "Canon" in device.product_name:
                # Získanie cesty k zariadeniu
                source_dir = device.device_path
                device.close()
                copy_photos(source_dir, destination_folder)
                return
        time.sleep(1)

def main():
    monitoring_thread = threading.Thread(target=monitor_usb)
    monitoring_thread.start()
    print("Monitoring for Canon EOS R6 connections...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
