from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, Qt , QSize,QTimer, QDateTime
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,QPushButton, QVBoxLayout \
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget\
    ,QTableWidgetItem,QHeaderView




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table")

        self.setFixedSize(QSize(800,500))
        self.setStyleSheet("background-color: #B4B4B4;")
        
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(vBox)

# ---------------------------------------------------------------------------------------------------------------------------------------------



        # Table 
        demo_data = [
            ['John', 'Doe', 'HR', 'Full-time', 75, 85, 'Pass', '2024-08-28'],
            ['Jane', 'Smith', 'IT', 'Part-time', 65, 70, 'Fail', '2024-08-28'],
            ['Alice', 'Johnson', 'Marketing', 'Intern', 90, 88, 'Pass', '2024-08-28']
        ]
        headers = [ 'Name', 'LastName', 'Department', 'Type','Left Score', 'Right Score', 'Result', 'Date testing', 'Delete']
        self.table = QTableWidget(len(demo_data),len(headers))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Don't edit data in table


        # Set Header Table
        for i ,h in enumerate(headers):
            self.table.setHorizontalHeaderItem(i,QTableWidgetItem(h))

        # fill out Data in table
        for row_index, row_data in enumerate(demo_data):
            for column_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;  /* Background color of the table */
                border: 1px solid #aaa;     /* Border around the table */
                gridline-color: #dddddd;       /* Color of the grid lines */
            }
            QTableWidget::item {
                padding: 5px;               /* Padding inside each cell */
                border: 1px solid #dddddd;     /* Border around each cell */
            }
            QHeaderView::section {
                background-color: #505558;  /* Background color of header sections */
                color: white;               /* Text color of header sections */
                padding: 5px;               /* Padding inside header sections */
                border: 1px solid #2e3a42;  /* Border around header sections */
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #a8d8d8;  /* Background color of selected items */
                color: black;               /* Text color of selected items */
            }
        """)

        # Icon delete
        iconDelete = QLabel()
        iconDelete.setPixmap(QPixmap('trash.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        iconDelete.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconDelete.setStyleSheet("""
            QLabel {
                background-color: transparent; /* Background color of the icon */
            }
        """)
        self.table.setCellWidget(0,8,iconDelete)

        vBox.addWidget(self.table)

        # Footer Layout
        hBoxFooter = QHBoxLayout()
        vBox.addLayout(hBoxFooter)

        self.backBtn = QPushButton('Back')
        self.backBtn.setStyleSheet('''
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
        hBoxFooter.addWidget(self.backBtn)
  

app = QCoreApplication.instance()
if app is None: app = QApplication([])


window = MainWindow()
window.show()
app.exec()