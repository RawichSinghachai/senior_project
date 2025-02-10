from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget, QHBoxLayout,
    QTableWidgetItem, QHeaderView
)

from database.database import Database


class DetailPage(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget
        self.db = Database()
        self.listUsers = []

        self.setFixedSize(QSize(800, 500))
        self.setStyleSheet("background-color: #B4B4B4;")


        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        

        self.title = QLabel('User Test Results')
        self.title.setStyleSheet("font-size: 30px; font-weight: bold;")
        vBox.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)


        # Define Table Headers
        headers = [
            'FirstName', 'LastName', 'Gender', 'Department', 'Position', 'Email', 'BirthDate',
            'LeftHandFrontScore', 'LeftHandBackScore', 'RightHandFrontScore', 'RightHandBackScore', 
            'totalScore', 'testingDate', 'Delete'
        ]

        # Setup Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setFixedSize(700, 300)  # กำหนดความกว้าง 800px และความสูง 400px


        # Auto Resize Columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Set Headers
        for i, h in enumerate(headers):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(h))
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #dddddd;
            }
            QHeaderView::section {
                background-color: #505558;
                color: white;
                padding: 5px;
                border: 1px solid #2e3a42;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #a8d8d8;
                color: black;
            }
        """)
        vBox.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignVCenter)

        # Back Button
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
        self.backBtn.clicked.connect(self.backPage)
        vBox.addWidget(self.backBtn)

    def backPage(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))

    def setUseId(self, user_id):
        """ ดึงข้อมูลจาก Database ตาม UserId และอัปเดตตาราง """
        if user_id:
            self.listUsers = self.db.getUserData(user_id)
            self.updateTable()


    def updateTable(self):
        """ อัปเดตข้อมูลใน QTableWidget """
        self.table.setRowCount(len(self.listUsers))

        for row_index, user in enumerate(self.listUsers):
            row_data = [
                user['FirstName'], user['LastName'], user['Gender'], user['Department'], 
                user['Position'], user['Email'], user['BirthDate'],
                user['LeftHandFrontScore'], user['LeftHandBackScore'], user['RightHandFrontScore'], 
                user['RightHandBackScore'], user['TotalScore'], user['TestingDate']
            ]
            # UserId = user['UserId']

            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, col_index, item)

            # Add Delete Icon
            iconDelete = QLabel()
            iconDelete.setPixmap(QPixmap('trash.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
            iconDelete.setAlignment(Qt.AlignmentFlag.AlignCenter)
            iconDelete.setStyleSheet("background-color: transparent;")
            self.table.setCellWidget(row_index, len(row_data), iconDelete)
