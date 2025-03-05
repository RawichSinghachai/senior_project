from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import ( QWidget, QLabel, QPushButton, QVBoxLayout )

from database.database import Database
from components.tableUi import TableUi


class DetailPage(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget
        self.db = Database()
        self.headers = [
            'FirstName', 'LastName', 'Gender', 'Department', 'Position', 'Email', 'BirthDate',
            'LeftHandFrontScore', 'LeftHandBackScore', 'RightHandFrontScore', 'RightHandBackScore', 
            'TotalScore', 'TestingDate', 'Delete'
        ]
        self.listUsers = []


        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBox.setSpacing(40)
        self.setLayout(vBox)
 
        
        self.title = QLabel('User Test Results')
        self.title.setStyleSheet("font-size: 30px; font-weight: bold;")
        vBox.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
      
        
        # Setup Table
        self.tableDetail = TableUi(self.headers, self.listUsers, 1200, 800)
        vBox.addWidget(self.tableDetail)

        # Back Button
        self.backBtn = QPushButton('Back')
        self.backBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
        self.backBtn.clicked.connect(self.backPage)
        vBox.addWidget(self.backBtn)

    def backPage(self):
        # รีเซ็ตตำแหน่ง Horizontal Scroll Bar ของ TableUi
        self.tableDetail.table.horizontalScrollBar().setValue(0)
        
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))

    def setUserId(self, user_id):
        """ ดึงข้อมูลจาก Database ตาม UserId และอัปเดตตาราง """
        if user_id:
            self.listUsers = self.db.getUserData(user_id)
            self.tableDetail.updateTable(self.listUsers)
