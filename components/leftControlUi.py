from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import  Qt, QTimer, QDateTime
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (QWidget, QLabel,QPushButton, QVBoxLayout)

class LeftControlUi(QWidget):
    def __init__(self):
        super().__init__()

        vBoxLeft = QVBoxLayout()
        vBoxLeft.setAlignment(Qt.AlignmentFlag.AlignTop)
        vBoxLeft.setSpacing(10)
        self.setLayout(vBoxLeft)

        # Profile Image
        img = QPixmap('assets/profile.png')
        img = img.scaled(250 , 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        lableImage = QLabel()
        lableImage.setPixmap(img)
        vBoxLeft.addWidget(lableImage, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Edit Button
        self.editBtn = QPushButton('Edit Profile')
        self.editBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.editBtn.setStyleSheet('''
            QPushButton {
                background-color:#000000;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#444444                
            }                 
            ''')
        vBoxLeft.addWidget(self.editBtn) 


        # Add User Button
        self.detailBtn = QPushButton('Detail')
        self.detailBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.detailBtn.setStyleSheet('''
            QPushButton {
                background-color:#000000;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#444444                
            }                 
            ''')
        vBoxLeft.addWidget(self.detailBtn) 


        # Start Button
        self.startBtn = QPushButton('Start Tetsing') 
        self.startBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.startBtn.setStyleSheet('''
            QPushButton {
                background-color:#6af21c;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#90f259              
            }                 
            ''')
        vBoxLeft.addWidget(self.startBtn) 

        # Exit Button
        self.exitBtn = QPushButton('Exit Program') 
        self.exitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.exitBtn.setStyleSheet('''
            QPushButton {
                background-color:#ff0000;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#fa4343             
            }                 
            ''')
        vBoxLeft.addWidget(self.exitBtn) 

        # lable timer
        self.dateLable = QLabel()
        self.dateLable.setStyleSheet("font-size: 10px; ")  # Optional styling
        vBoxLeft.addWidget(self.dateLable)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        self.updateDateTime()

    # funtion timer
    def updateDateTime(self):
        # Get the current date and time
        current_date_time = QDateTime.currentDateTime()
        # Format it to display as needed
        formatted_date_time = current_date_time.toString("dddd, MMMM d, yyyy hh:mm:ss AP")
        # Update the QLabel with the current date and time
        self.dateLable.setText(formatted_date_time)      
    