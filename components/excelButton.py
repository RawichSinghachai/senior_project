from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import QCoreApplication, Qt , QSize,QTimer, QDateTime
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView)

class ExcelButton(QWidget):
    def __init__(self):
        super().__init__()

        hBoxExcel = QHBoxLayout()
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