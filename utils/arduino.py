import serial.tools.list_ports
import serial
import time

class ArduinoController:
    def __init__(self):
        self.arduino = None
        self.arduino_port = self.find_arduino_port()

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "ACM" in port.device or "COM" in port.device or "USB" in port.device:  # รองรับทั้ง Linux และ Windows
                return port.device
        return None

    def connect(self):
        if self.arduino_port:
            try:
                self.arduino = serial.Serial(self.arduino_port, baudrate=9600, timeout=1)
                print(f"✅ Arduino connected on {self.arduino_port}")
            except serial.SerialException as e:
                print(f"❌ Error connecting to Arduino: {e}")
        else:
            print("❌ Arduino not found")

    def send_command(self, command):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(f"{command}\n".encode())
                time.sleep(0.1)
                if self.arduino.in_waiting > 0:
                    response = self.arduino.readline().decode('utf-8').strip()
                    print(f"🔹 Arduino Response: {response}")
                else:
                    print("⚠️ No data received from Arduino")
            except serial.SerialException as e:
                print(f"❌ Error communicating with Arduino: {e}")

    def close_connection(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("🔌 Serial connection closed")
