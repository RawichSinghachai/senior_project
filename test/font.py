from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # โหลดฟอนต์จากไฟล์
        font_id1 = QFontDatabase.addApplicationFont("fonts/Sarabun-Regular.ttf")  # ฟอนต์ไทย
        font_id2 = QFontDatabase.addApplicationFont("fonts/Roboto-Regular.ttf")  # ฟอนต์อังกฤษ

        # ดึงชื่อฟอนต์
        font_family1 = QFontDatabase.applicationFontFamilies(font_id1)[0] if font_id1 != -1 else "Sans Serif"
        font_family2 = QFontDatabase.applicationFontFamilies(font_id2)[0] if font_id2 != -1 else "Sans Serif"

        # สร้าง QLabel พร้อมกำหนดฟอนต์
        label_th = QLabel("ภาษาไทย: สวัสดีครับ/ค่ะ")
        label_th.setFont(QFont(font_family1, 20))  # ใช้ฟอนต์ Sarabun

        label_en = QLabel("English: Hello, World!")
        label_en.setFont(QFont(font_family2, 20))  # ใช้ฟอนต์ Roboto

        layout.addWidget(label_th)
        layout.addWidget(label_en)

        self.setLayout(layout)

app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())
