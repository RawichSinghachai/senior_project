from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QPushButton, QHBoxLayout)

class ExcelButton(QWidget):
    def __init__(self):
        super().__init__()

        hBoxExcel = QHBoxLayout()
        hBoxExcel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hBoxExcel.setSpacing(20)
        self.setLayout(hBoxExcel)

        # Import Excel Button
        self.importExcelBtn = QPushButton('Import Excel')
        self.importExcelBtn.setFixedWidth(250)
        self.importExcelBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.importExcelBtn.setStyleSheet('''
            QPushButton {
                background-color:#0086ff;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#72b9fa                
            }                 
            ''')
        hBoxExcel.addWidget(self.importExcelBtn)


        # Export Excel Button
        self.exportExcelBtn = QPushButton('Export Excel')
        self.exportExcelBtn.setFixedWidth(250)
        self.exportExcelBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.exportExcelBtn.setStyleSheet('''
            QPushButton {
                background-color:#0086ff;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#72b9fa                
            }                 
            ''')
        hBoxExcel.addWidget(self.exportExcelBtn)