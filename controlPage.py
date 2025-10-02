from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox,QFileDialog)
from PyQt6.QtGui import QMouseEvent, QShowEvent
import pandas as pd
import uuid


from database.database import Database
from components.tableUi import TableUi
from components.leftControlUi import LeftControlUi
from components.searchBar import SearchBar
from components.excelButton import ExcelButton
from utils.messageBox import showMessageBox,showMessageDeleteDialog  
from utils.excelRender import excelRender




class ControlPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget

        # Database ------------------------------------------------------------------------------------
        self.db = Database.getInstance()
        self.headers = ['FirstName', 'LastName', 'Department', 'Position', 'Email', 'Gender', 'BirthDate', 'Delete']
        self.listUsers = self.db.getAllUser() or []
        
        hBox = QHBoxLayout()
        hBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(hBox)
        
        # Left ----------------------------------------------------------------------------------------------------
        self.leftControlUi = LeftControlUi()
        hBox.addWidget(self.leftControlUi)
        

# ---------------------------------------------------------------------------------------------------------------------------------------------
        # Right
        vBoxRight = QVBoxLayout()
        hBox.addLayout(vBoxRight)

        #  SeachBar 
        self.searchBar = SearchBar()
        vBoxRight.addWidget(self.searchBar)



        # Table
        self.tableUi = TableUi(self.headers, self.listUsers, 800, 600)
        vBoxRight.addWidget(self.tableUi)
        # print(self.listUsers)

        # Excel
        self.excelButton = ExcelButton()
        vBoxRight.addWidget(self.excelButton)

      
        # Get instance
        self.leftControlUi.editBtn.clicked.connect(self.openEditPage)
        self.leftControlUi.detailBtn.clicked.connect(self.openDetailPage)
        self.leftControlUi.startBtn.clicked.connect(self.openProgressPage)
        self.leftControlUi.exitBtn.clicked.connect(self.closeProgram)
        self.searchBar.searchBtn.clicked.connect(self.filterTable)
        self.searchBar.searchInput.returnPressed.connect(self.filterTable)
        self.searchBar.clearBtn.clicked.connect(self.clearFilterTable)
        self.excelButton.importExcelBtn.clicked.connect(self.importExcelFile)
        self.excelButton.exportExcelBtn.clicked.connect(self.exportExcelFile)
        self.excelButton.DeleteTableBtn.clicked.connect(self.deleteTable)
        




    # Logic ---------------------------------------------------------------------------------------
        
        for user_id, iconDelete in self.tableUi.iconDeleteDict.items():
            iconDelete.mousePressEvent = lambda event, uid=user_id: self.deleteRow(event, uid)


    # เรียก refreshPage ทุกครั้งที่ ControlPage ถูกแสดง
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.refreshPage()
            

    # Open Edit Page
    def openEditPage(self):
        self.rowTable = self.tableUi.getRowData()
        edit_page = self.stackedWidget.widget(3)
        edit_page.populateForm(self.rowTable)
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(3))
        

    def openDetailPage(self):
        if not self.tableUi.getRowData().get('UserId'):
            return
        detail_page = self.stackedWidget.widget(4)
        detail_page.setUserId(self.tableUi.getRowData()['UserId'])
        self.stackedWidget.setCurrentWidget(detail_page)

    # Open Progress page
    def openProgressPage(self):
        # Don't have UserId
        if not self.tableUi.getRowData().get('UserId'):
            self.userId = uuid.uuid4()
            process_page = self.stackedWidget.widget(5)
            process_page.setUserId(self.userId)
            self.stackedWidget.setCurrentWidget(process_page)
        else:    
            # Have UserId(Registered)
            process_page = self.stackedWidget.widget(5) 
            process_page.setUserId(self.tableUi.getRowData()['UserId'])
            self.stackedWidget.setCurrentWidget(process_page)


    # Delete Account
    def deleteRow(self, event: QMouseEvent, user_id):
        # print("Delete Row ??")
        if event.button() == Qt.MouseButton.LeftButton:

            response = showMessageDeleteDialog(self)
            if response == QMessageBox.StandardButton.Yes:
                # print(f'Delete clicked for UserId: {user_id}')
                if self.db.deleteUser(user_id):
                    self.tableUi.rowData = {}
                    self.tableUi.selectedRowIndex = None
                    # Refresh Control Page
                    self.refreshPage()
                    showMessageBox('Delete','User  deleted successfully.')

            
                else:
                    showMessageBox('Delete','Failed to delete user',mode=('error'))
            else:
                pass
                # print('User canceled the deletion.')


    # Refresh Control Page
    def refreshPage(self):
        # print('Refresh Control Page')
        self.listUsers = self.db.getAllUser()  # ดึงข้อมูลใหม่จากฐานข้อมูล
        self.tableUi.updateTable(self.listUsers)  # อัปเดตตาราง
        self.tableUi.deSelectionRow()  # Clear selection in table

        for user_id, iconDelete in self.tableUi.iconDeleteDict.items():
            iconDelete.mousePressEvent = lambda event, uid=user_id: self.deleteRow(event, uid)

    def filterTable(self):

        filterSearch = self.searchBar.comboBoxSeachInput.currentText()

        search_text = self.searchBar.searchInput.text()
        if not search_text :
            self.clearFilterTable()
            return
        listUsers = self.db.searchUser(search_text, filterSearch)
        self.tableUi.updateTable(listUsers)

    def clearFilterTable(self):
        self.searchBar.searchInput.clear()
        self.searchBar.comboBoxSeachInput.setCurrentIndex(0)
        listUsers = self.db.searchUser("")
        self.tableUi.updateTable(listUsers)
        


    def exportExcelFile(self):
        try:
            excelRender(self.db.getAllUserData())
            showMessageBox('Export Excel','Export excel successfully.',mode='info')
            # print('export excel already')
        except Exception as e:
            showMessageBox('Export Excel','Export excel unsuccessfully.',mode='error')

    def closeProgram(self):
        QApplication.instance().quit()

        
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

            # print(f"File Content Preview:\n{users_excel}")
            self.refreshPage()
        except Exception as e:
            pass
            # print(f"Error reading file:\n{e}")

    def deleteTable(self):
        response = showMessageDeleteDialog(self, 'Delete All Account', 'Are you sure you want to delete all items?')
        if response == QMessageBox.StandardButton.Yes:
            self.db.deleteAllUser()
            self.refreshPage()
        else:
            pass

