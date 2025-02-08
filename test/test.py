import serial.tools.list_ports



def find_uart_ports():
    ports = serial.tools.list_ports.comports()
    uart_ports = []
    for port in ports:
        uart_ports.append((port.device, port.description))
    return uart_ports

if __name__ == "__main__":
    uart_ports = find_uart_ports()
    if uart_ports:
        print("Found UART ports:")
        for device, description in uart_ports:
            print(f"Port: {device}, Description: {description}")
    else:
        print("No UART ports found.")

