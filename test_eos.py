import win32api
import win32con
import win32com.client

def is_camera_connected():
    # GUID pre USB zariadenia
    usb_guid = "{A5DCBF10-6530-11D2-901F-00C04FB951ED}"
    
    # Získanie zoznamu pripojených USB zariadení
    devices = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".").ExecQuery(
        "SELECT * FROM Win32_PnPEntity WHERE ClassGuid = '" + usb_guid + "'")
    
    # Prehľadávanie zoznamu zariadení a hľadanie kamerového zariadenia
    for device in devices:
        if "Canon EOS R6" in str(device.Caption):
            return True  # Nájdená kamera Canon EOS R6
    
    return False  # Kamera Canon EOS R6 nie je pripojená

# Testovanie funkcie is_camera_connected()
if is_camera_connected():
    print("Kamera Canon EOS R6 je pripojená.")
else:
    print("Kamera Canon EOS R6 nie je pripojená.")
