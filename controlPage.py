from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, Qt , QSize,QTimer, QDateTime
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView,QFileDialog)
from PyQt6.QtGui import QMouseEvent
import pandas as pd

from database.database import Database
from tableUi import TableUi
from leftControlUi import LeftControlUi
from utils.seachBar import SeachBar
from excelButton import ExcelButton
from utils.messageBox import showMessageBox,showMessageDeleteDialog  
from excelRender import excelRender
from utils.vision import main




class ControlPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget

        # Database ------------------------------------------------------------------------------------
        self.db = Database()
        self.listUsers = self.db.getAllUser()

        # Title Window
        self.setWindowTitle("Table")

        # self.setFixedSize(QSize(800,500))
        self.setStyleSheet("background-color: #B4B4B4;")
        
        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(hBox)
        
        # Left ----------------------------------------------------------------------------------------------------
        self.leftControlUi = LeftControlUi()
        hBox.addWidget(self.leftControlUi)
        

# ---------------------------------------------------------------------------------------------------------------------------------------------
        # Right
        vBoxRight = QVBoxLayout()
        vBoxRight.setAlignment(Qt.AlignmentFlag.AlignTop)
        hBox.addLayout(vBoxRight)

        #  SeachBar 
        self.searchBar = SeachBar()
        vBoxRight.addWidget(self.searchBar)

        # Table
        self.tableUi = TableUi(self.listUsers)
        vBoxRight.addWidget(self.tableUi)
        # print(self.listUsers)

        # Excel
        self.excelButton = ExcelButton()
        vBoxRight.addWidget(self.excelButton)

      
        # Get instance
        self.leftControlUi.editBtn.clicked.connect(self.openEditPage)
        self.leftControlUi.detailBtn.clicked.connect(self.openDetailPage)
        self.leftControlUi.startBtn.clicked.connect(self.openProgressPage)
        self.searchBar.searchInput.textChanged.connect(self.filterTable)
        self.excelButton.importExcelBtn.clicked.connect(self.importExcelFile)
        self.excelButton.exportExcelBtn.clicked.connect(self.exportExcelFile)




    # Logic ---------------------------------------------------------------------------------------

        for user_id, iconDelete in self.tableUi.iconDeleteDict.items():  # Fix here by accessing the dictionary
            iconDelete.mousePressEvent = lambda event, uid=user_id: self.deleteRow(event, uid)
 
    #     self.updateButtonState()
        
    # def updateButtonState(self):
    #     """ ปิดการใช้งานปุ่ม detailBtn และ startBtn หากไม่มี UserId """
    #     row_data = self.tableUi.getRowData()
    #     has_user = bool(row_data and row_data.get('UserId'))

    #     self.leftControlUi.detailBtn.setEnabled(has_user)
    #     self.leftControlUi.startBtn.setEnabled(has_user)

    # Open Edit Page
    def openEditPage(self):
        edit_page = self.stackedWidget.widget(3)
        edit_page.populateForm(self.tableUi.getRowData())
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(3))
        

    def openDetailPage(self):
        if not self.tableUi.getRowData().get('UserId'):
            return
        detail_page = self.stackedWidget.widget(4)
        detail_page.setUseId(self.tableUi.getRowData()['UserId'])
        self.stackedWidget.setCurrentWidget(detail_page)

    # Open Progress page
    def openProgressPage(self):
        if not self.tableUi.getRowData().get('UserId'):
            return
        process_page = self.stackedWidget.widget(5)  # ดึง widget จาก stackedWidget
        process_page.setUserId(self.tableUi.getRowData()['UserId'])
        self.stackedWidget.setCurrentWidget(process_page)
        # area = main()
        # self.db.creatUserTesting(self.tableUi.getRowData()['UserId'],area)
        # write area to database
        # process_page.loading_success(area)


    # Delete Account
    def deleteRow(self, event: QMouseEvent, user_id):
        if event.button() == Qt.MouseButton.LeftButton:

            response = showMessageDeleteDialog(self)
            if response == QMessageBox.StandardButton.Yes:
                print(f'Delete clicked for UserId: {user_id}')
                if self.db.deleteUser(user_id):
                    showMessageBox('Delete','User  deleted successfully.')
                    # Refresh Control Page
                    self.refreshControlPage()

            
                else:
                    showMessageBox('Delete','Failed to delete user',mode=('error'))
            else:
                print('User canceled the deletion.')


    # Refresh Control Page
    def refreshControlPage(self):
        index = self.stackedWidget.indexOf(self)  # Store the index of the current ControlPage  
        new_control_page = ControlPage(self.stackedWidget)  # Create a new ControlPage  
        self.stackedWidget.removeWidget(self)  # Remove the old ControlPage  
        self.stackedWidget.insertWidget(index, new_control_page)  # Insert the new ControlPage at the same index  
        self.stackedWidget.setCurrentWidget(new_control_page)  # Switch to the new ControlPage  



    def filterTable(self):
        pass

    def exportExcelFile(self):
        excelRender(self.db.getAllUserData())
        print('export excel already')


        
    def importExcelFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Excel File", 
            "", 
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if file_path:
            print(f"Selected File: {file_path}")
            self.read_excel(file_path)
        else:
            print("No file selected")


    def read_excel(self, file_path):
        try:
            # Read Excel file using pandas
            df = pd.read_excel(file_path)
            
            # Show the first few rows
            users_excel = df.to_dict(orient="records")

            self.db.import_users(users_excel)

            print(f"File Content Preview:\n{users_excel}")
            self.refreshControlPage()
        except Exception as e:
            print(f"Error reading file:\n{e}")


    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Exit Confirmation', 'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Program is closing...")  # รันคำสั่งเมื่อปิด
            event.accept()  # อนุญาตให้ปิด
        else:
            event.ignore()  # ยกเลิกการปิดโปรแกรม


# app = QCoreApplication.instance()
# if app is None: app = QApplication([])


# window = ControlPage()
# window.show()
# app.exec()