from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QLineEdit, QComboBox)

class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        self.header = ["FirstName", "LastName", "Department", "Position", "Email", "Gender", "BirthDate"]

        hBoxSeach = QHBoxLayout()
        hBoxSeach.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hBoxSeach.setSpacing(20)
        self.setLayout(hBoxSeach)

        # ComboBox
        self.comboBoxSeachInput = QComboBox()
        self.comboBoxSeachInput.addItems(self.header)
        self.comboBoxSeachInput.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboBoxSeachInput.setMinimumWidth(50)
        self.comboBoxSeachInput.setStyleSheet("""
            QComboBox {
                background-color: #F0F0F0;
                border-radius: 5px;
                padding: 5px;
                font: 14px Arial;
            }
            QComboBox::drop-down {
                width: 25px;
            }
            QComboBox::down-arrow {
                image: url(assets/caret-down.png); /* Custom arrow icon */
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #F0F0F0;
                selection-background-color: #5A9;
                selection-color: #000000;
            }
        """)
        hBoxSeach.addWidget(self.comboBoxSeachInput)

        #  Search LineEdit
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search...")
        self.searchInput.setMinimumWidth(300)
        self.searchInput.setMaximumWidth(800) 
        self.searchInput.setStyleSheet("""
            QLineEdit {
                border-radius: 5px; /* Rounded corners */
                padding: 10px; /* Padding inside the widget */
                font-size: 14px; /* Font size */
                background-color: #f9f9f9; /* Background color */
            }
        """)

        hBoxSeach.addWidget(self.searchInput)

        # Seach Button
        self.searchBtn = QPushButton('Search')
        self.searchBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.searchBtn.setFixedWidth(100)
        self.searchBtn.setStyleSheet('''
            QPushButton {
                background-color:#f50722;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#f75a6c                
            }                 
            ''')
        hBoxSeach.addWidget(self.searchBtn)

        # Clear Button
        self.clearBtn = QPushButton('Clear')
        self.clearBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clearBtn.setFixedWidth(100)
        self.clearBtn.setStyleSheet('''
            QPushButton {
                background-color:#f50722;
                color:white;
                padding:10px;
                font-size:16px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color:#f75a6c                
            }                 
            ''')
        hBoxSeach.addWidget(self.clearBtn)