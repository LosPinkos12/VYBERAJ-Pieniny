import usb.core
import usb.util

# Nájdenie zariadenia Canon EOS R6
def find_canon_eos():
    vendor_id = 0x04a9  # ID výrobcu Canon
    product_id = 0x32fb  # ID produktu pre Canon EOS R6

    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    return device

# Funkcia na čítanie dát z zariadenia
def read_data(device):
    try:
        # Otvorenie zariadenia
        device.set_configuration()
        
        # Príklad čítania dát
        endpoint = device[0][(0,0)][0]
        data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        
        print("Prečítané dáta:", data)
    except usb.core.USBError as e:
        print("Chyba pri čítaní dát:", e)

# Hlavná funkcia
def main():
    device = find_canon_eos()
    if device is None:
        print("Fotoaparát Canon EOS R6 nebol nájdený.")
        return
    
    print("Fotoaparát Canon EOS R6 bol úspešne nájdený.")
    
    # Tu môžete volať ďalšie funkcie na prácu so zariadením, napr. read_data(device)
    # Zabezpečte, aby ste zavolali usb.util.dispose_resources(device) na konci práce so zariadením.

if __name__ == '__main__':
    main()
