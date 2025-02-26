import sys
import serial.tools.list_ports
import serial
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class ArduinoControl(QWidget):
    def __init__(self):
        super().__init__()

        self.arduino = None  # ตัวแปรเก็บการเชื่อมต่อ Serial
        self.init_ui()
        self.connect_arduino()

    def init_ui(self):
        """สร้าง UI"""
        self.setWindowTitle("Arduino Control")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel("🔍 กำลังค้นหา Arduino...")
        layout.addWidget(self.status_label)

        self.btn_on = QPushButton("🔴 Turn On")
        self.btn_on.clicked.connect(self.turn_on)
        layout.addWidget(self.btn_on)

        self.btn_off = QPushButton("⚪ Turn Off")
        self.btn_off.clicked.connect(self.turn_off)
        layout.addWidget(self.btn_off)

        self.response_label = QLabel("📡 Arduino Response: -")
        layout.addWidget(self.response_label)

        self.setLayout(layout)

    def connect_arduino(self):
        """ค้นหาและเชื่อมต่อ Arduino"""
        arduino_port = "COM6"
        if arduino_port:
            try:
                self.arduino = serial.Serial(arduino_port, baudrate=9600, timeout=1)
                self.status_label.setText(f"✅ Arduino เชื่อมต่อที่ {arduino_port}")
            except serial.SerialException as e:
                self.status_label.setText(f"❌ ไม่สามารถเชื่อมต่อ: {e}")
        else:
            self.status_label.setText("❌ ไม่พบ Arduino")

    def find_arduino_port(self):
        """ค้นหาพอร์ตของ Arduino"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "ACM" in port.device or "USB" in port.device:
                return port.device
        return None

    def send_command(self, command):
        """ส่งคำสั่งไปยัง Arduino"""
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(f"{command}\n".encode())  # ส่งข้อมูล
                time.sleep(0.1)  # รอให้ Arduino ตอบกลับ
                if self.arduino.in_waiting > 0:
                    response = self.arduino.readline().decode().strip()
                    self.response_label.setText(f"📡 Arduino Response: {response}")
                else:
                    self.response_label.setText(f"📡 Arduino Response: (No Data)")
            except serial.SerialException as e:
                self.response_label.setText(f"⚠️ Error: {e}")
        else:
            self.response_label.setText("❌ Arduino ไม่เชื่อมต่อ")

    def turn_on(self):
        """ส่งคำสั่งเปิดไปยัง Arduino"""
        self.send_command("on")

    def turn_off(self):
        """ส่งคำสั่งปิดไปยัง Arduino"""
        self.send_command("off")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArduinoControl()
    window.show()
    sys.exit(app.exec())
