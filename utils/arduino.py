import serial.tools.list_ports
import serial
import time

from logger import AppLogger

class ArduinoController:
    def __init__(self):
        self.arduino = None
        self.arduino_port = self.find_arduino_port()
        self.logger = AppLogger().get_logger()

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "ACM" in port.device or "COM" in port.device:  # รองรับทั้ง Linux และ Windows
                self.logger.info(f"Arduino found on {port.device}") # Log
                return port.device
        self.logger.error("Arduino not found port") # Log
        return None

    def connect(self):
        if self.arduino_port:
            try:
                self.arduino = serial.Serial(self.arduino_port, baudrate=9600, timeout=1)
                self.logger.info(f"Arduino connected on {self.arduino_port}") # Log
            except serial.SerialException as e:
                self.logger.error(f"Error connecting to Arduino: {e}") # Log
        else:
            self.logger.error("Arduino not found") # Log

    def send_command(self, command):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(f"{command}\n".encode())
                time.sleep(0.1)
                if self.arduino.in_waiting > 0:
                    response = self.arduino.readline().decode('utf-8').strip()
                    self.logger.info(f"Arduino Response: {response}") # Log
                else:
                    self.logger.warning("No data received from Arduino") # Log
            except serial.SerialException as e:
                self.logger.error(f"Error communicating with Arduino: {e}") # Log

    def close_connection(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            self.logger.info("Serial connection closed") # Log

