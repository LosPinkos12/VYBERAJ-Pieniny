import os
import shutil
import time
import threading
import pywinusb.hid as hid

# Destination folder where photos will be copied
destination_folder = r"C:\path\to\your\folder"

def copy_photos(source_dir, dest_dir):
    print(f"Copying photos from {source_dir} to {dest_dir}")
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            shutil.copy(os.path.join(source_dir, filename), dest_dir)
            print(f"Copied {filename}")

def monitor_usb():
    # Define the USB vendor and product IDs for Canon EOS R6
    vendor_id = 0x04a9  # Canon vendor ID
    product_id = 0x32fb  # Canon EOS R6 product ID

    # Find all USB HID devices
    all_devices = hid.find_all_hid_devices()

    while True:
        for device in all_devices:
            if device.vendor_id == vendor_id and device.product_id == product_id:
                print("Canon EOS R6 detected.")
                try:
                    device.open()
                    source_dir = device.device_path
                    device.close()
                    copy_photos(source_dir, destination_folder)
                except Exception as e:
                    print(f"Error accessing device: {e}")
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
