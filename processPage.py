from PyQt6.QtCore import (Qt, QSize, QThread, pyqtSignal, QTimer)
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout)
from utils.vision import main
from database.database import Database

class VisionThread(QThread):
    hand_data_signal = pyqtSignal(dict)
    result_signal = pyqtSignal(list)

    def run(self):
        """ เรียกใช้งาน main() และส่งข้อมูลผ่าน signal """
        main(self.hand_data_signal.emit, self.result_signal.emit)

class ProcessPage(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()

        # Database
        self.db = Database()
        self.stackedWidget = stackedWidget
        self.user_id = None
        self.visionThread = None
        self.is_camera_running = False  

        self.setFixedSize(QSize(800, 500))
        self.setStyleSheet("background-color: #B4B4B4;")

        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        self.title = QLabel('Testing Hand Hygiene')
        self.title.setStyleSheet("font-size: 30px; font-weight: bold;")
        vBox.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label_left = QLabel("Left Hand: Waiting...")
        self.label_right = QLabel("Right Hand: Waiting...")
        vBox.addWidget(self.label_left)
        vBox.addWidget(self.label_right)

        self.message = QLabel('IsLoading.....')
        self.message.setStyleSheet("font-size: 50px; font-weight: bold;")
        vBox.addWidget(self.message, alignment=Qt.AlignmentFlag.AlignCenter)

        self.area = QLabel('Area ....')
        self.area.setStyleSheet("font-size: 12px; font-weight: bold;")
        vBox.addWidget(self.area)

        self.backBtn = QPushButton('Back')
        self.backBtn.setStyleSheet('''
            QPushButton {
                background-color:#f75a6c;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#f50722                
            }                 
        ''')
        vBox.addWidget(self.backBtn)
        self.backBtn.clicked.connect(self.backPage)

    def backPage(self):
        """ กลับไปยังหน้าก่อนหน้า และปิดกล้อง """
        self.stopVisionProcessing()
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))

    def setUserId(self, user_id):
        if user_id:
            self.user_id = user_id

    def update_hand_data(self, hand_data):
        """ อัปเดต UI ตามข้อมูลที่ได้รับจาก vision """
        # self.label_left.setText(f"Left Hand: {hand_data.get('Left Hand', 'None')}")
        # self.label_right.setText(f"Right Hand: {hand_data.get('Right Hand', 'None')}")
        QTimer.singleShot(0, lambda: self.label_left.setText(f"Left Hand: {hand_data.get('Left Hand', 'None')}"))
        QTimer.singleShot(0, lambda: self.label_right.setText(f"Right Hand: {hand_data.get('Right Hand', 'None')}"))

    def handle_result(self, data):
        """ รับค่าที่ `main()` ส่งกลับมา """
        if data:
            QTimer.singleShot(0, lambda: self.area.setText(str(data)))  
            self.db.creatUserTesting(self.user_id, data)
            detail_page = self.stackedWidget.widget(4)
            detail_page.setUseId(self.user_id)
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(4))

    def startVisionProcessing(self):
        """ เริ่มต้นการประมวลผลกล้อง (เฉพาะตอนเปิดหน้านี้) """
        if not self.visionThread or not self.visionThread.isRunning():
            self.visionThread = VisionThread()
            self.visionThread.hand_data_signal.connect(self.update_hand_data)
            self.visionThread.result_signal.connect(self.handle_result)
            self.visionThread.start()
            self.is_camera_running = True

    def stopVisionProcessing(self):
        """ หยุดการประมวลผลกล้อง (ตอนออกจากหน้านี้) """
        if self.visionThread and self.visionThread.isRunning():
            self.visionThread.requestInterruption()
            self.visionThread.quit()
            self.visionThread.wait()
            self.visionThread = None
            self.is_camera_running = False

    def showEvent(self, event):
        """ เรียกใช้เมื่อ ProcessPage ถูกเปิด """
        self.startVisionProcessing()
        super().showEvent(event)

    def hideEvent(self, event):
        """ เรียกใช้เมื่อ ProcessPage ถูกซ่อน """
        self.stopVisionProcessing()
        super().hideEvent(event)
