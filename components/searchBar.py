from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, Qt , QSize,QTimer, QDateTime
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView)

class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        hBoxSeach = QHBoxLayout()
        self.setLayout(hBoxSeach)

        #  Search LineEdit
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search...")
        # self.searchInput.setFixedWidth(480)
        self.searchInput.setStyleSheet("""
            QLineEdit {
                border-radius: 5px; /* Rounded corners */
                padding: 10px; /* Padding inside the widget */
                font-size: 14px; /* Font size */
                background-color: #f9f9f9; /* Background color */
            }
        """)

        hBoxSeach.addWidget(self.searchInput)

        # button Search
        self.searchBtn = QPushButton('Search')
        # searchBtn.setFixedWidth(100)
        self.searchBtn.setStyleSheet('''
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
        hBoxSeach.addWidget(self.searchBtn)