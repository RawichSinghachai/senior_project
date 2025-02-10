from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import (QCoreApplication, Qt , QSize,QTimer, QDateTime,QDate)
from PyQt6.QtGui import (QColor)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView)
from PyQt6.QtGui import QMouseEvent

from utils.vision import main
from database.database import Database


class ProcessPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        # Database ------------------------------------------------------------------------------------
        self.db = Database()

        self.stackedWidget = stackedWidget
        self.user_id = None
        self.is_camera_running = False 

        self.setFixedSize(QSize(800, 500))
        self.setStyleSheet("background-color: #B4B4B4;")

        # self.user_data = {
        #     'firstName' : '',
        #     'lastName' : '',
        #     'email' : '',
        #     'department' : '',
        #     'gender' : '',
        #     'birthDate' : QDate.currentDate().toString('dd/MM/yyyy')
        # }

        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)


        self.title = QLabel('Testing Hand Hygiene')
        self.title.setStyleSheet(
            """
                font-size: 30px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.title,alignment=Qt.AlignmentFlag.AlignCenter)


        self.label_left = QLabel("Left Hand: Waiting...")
        self.label_right = QLabel("Right Hand: Waiting...")
        vBox.addWidget(self.label_left)
        vBox.addWidget(self.label_right)

        self.message = QLabel('IsLoading.....')
        self.message.setStyleSheet(
            """
                font-size: 50px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.message,alignment=Qt.AlignmentFlag.AlignCenter)

        self.area = QLabel('Area ....')
        self.area.setStyleSheet(
            """
                font-size: 12px;
                font-weight: bold;
            """
        )
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
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))


    def setUserId(self, user_id):
        if user_id:
            self.user_id = user_id
            data = main()
            self.db.creatUserTesting(self.user_id,data)
            detail_page = self.stackedWidget.widget(4)
            detail_page.setUseId(self.user_id)
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(4))
        

    def setTextMessage(self,message):
        self.message.setText(message)

            
