import serial.tools.list_ports

def find_usb_ports():
    ports = serial.tools.list_ports.comports()
    usb_ports = [
        (port.device, port.description)
        for port in ports
        if "USB" in port.description or "ACM" in port.device
    ]
    return usb_ports

if __name__ == "__main__":
    usb_ports = find_usb_ports()
    if usb_ports:
        print("Found USB UART ports:")
        for device, description in usb_ports:
            print(f"Port: {device}, Description: {description}")
    else:
        print("No USB UART ports found.")

