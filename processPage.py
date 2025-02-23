from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import (QCoreApplication, Qt , QSize,QTimer, QDateTime,QDate)
from PyQt6.QtGui import (QColor)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView)
from PyQt6.QtGui import QMouseEvent

from utils.vision import main
from database.database import Database
from utils.messageBox import showMessageBox



class ProcessPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        # Database ------------------------------------------------------------------------------------
        self.db = Database()

        self.stackedWidget = stackedWidget
        self.user_id = None
        self.is_camera_running = False 


        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBox.setSpacing(20)
        self.setLayout(vBox)


        self.title = QLabel('Testing Hand Hygiene')
        self.title.setStyleSheet(
            """
                font-size: 30px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.title,alignment=Qt.AlignmentFlag.AlignHCenter)



        self.message = QLabel('IsLoading.....')
        self.message.setStyleSheet(
            """
                font-size: 24px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.message,alignment=Qt.AlignmentFlag.AlignHCenter)


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
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))


    def setUserId(self, user_id):
        if user_id:
            self.user_id = user_id
            self.message.setText("Processing... Please wait.")
            # data = main()
            # self.db.creatUserTesting(self.user_id,data)
            QCoreApplication.processEvents()  # อัปเดต UI ทันที
            QTimer.singleShot(100, self.processUserTesting)


    def processUserTesting(self):
        data, err = main(self.user_id)  # เรียกใช้ main() ที่อาจใช้เวลานาน
        if  data:
            self.db.creatUserTesting(self.user_id, data)  # บันทึกข้อมูลใน DB
            detail_page = self.stackedWidget.widget(4)
            detail_page.setUserId(self.user_id)
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(4))
        elif err:
            showMessageBox("Error", err, "error")
            self.message.setText(f"Status : {err}")
            

