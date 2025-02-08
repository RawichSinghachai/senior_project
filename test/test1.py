from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QCalendarWidget, QLabel, QWidget
from PyQt6.QtCore import QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QCalendarWidget Example")
        
        # สร้าง Calendar Widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)  # แสดงเส้นตาราง
        self.calendar.setMinimumSize(400, 300)  # ปรับขนาดขั้นต่ำของ Calendar Widget
        self.calendar.clicked.connect(self.date_selected)
        
        # ปรับแต่งสไตล์ให้ปุ่มและ SpinBox ของ QCalendarWidget
        self.calendar.setStyleSheet("""
            QCalendarWidget QToolButton {
                min-width: 50px;  /* ความกว้างขั้นต่ำของปุ่ม */
                min-height: 25px; /* ความสูงขั้นต่ำของปุ่ม */
                font-size: 14px;  /* ขนาดฟอนต์ */
                color: white;     /* สีของตัวอักษร */
                background-color: #005a9e; /* สีพื้นหลังของปุ่ม */
                border: none;     /* ไม่มีขอบ */
                border-radius: 5px; /* มุมโค้ง */
            }
            QCalendarWidget QToolButton:hover {
                background-color: #0078d7; /* สีเมื่อเอาเมาส์ไปชี้ */
            }
            QCalendarWidget QSpinBox {
                min-width: 100px;  /* ความกว้างขั้นต่ำของ SpinBox */
                font-size: 12px;   /* ขนาดฟอนต์ */
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color:#e619c0; /* สีพื้นหลังของ Navigation Bar */
            }
        """)

        # สร้าง Label สำหรับแสดงวันที่ที่เลือก
        self.label = QLabel("Selected Date: None")
        self.label.setStyleSheet("font-size: 16px; color: #333;")

        # สร้าง Layout และใส่ Widget ทั้งหมด
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.label)
        
        # สร้าง QWidget และใส่ Layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def date_selected(self, date: QDate):
        # อัปเดต Label เมื่อเลือกวันที่
        self.label.setText(f"Selected Date: {date.toString('yyyy-MM-dd')}")

# สร้างแอปพลิเคชัน
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
