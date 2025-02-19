from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import (QCoreApplication, Qt , QSize,QTimer, QDateTime,QDate)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView,QDateEdit,QComboBox, QSizePolicy)

from components.editUserUi import EditUserUi
from database.database import Database
from utils.messageBox import showMessageBox
from controlPage import ControlPage
from utils.logger import AppLogger


class EditPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget
        
        vBox = QVBoxLayout()
        vBox.setAlignment( Qt.AlignmentFlag.AlignCenter)
        vBox.setSpacing(20)
        self.setLayout(vBox)

        # StepUp Logger
        self.logger = AppLogger().get_logger()

        self.title = QLabel('Edit Profile')
        self.title.setStyleSheet(
            """
                font-size: 30px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)

        
        

        # Form Login
        self.formEditUi =  EditUserUi()
        vBox.addWidget(self.formEditUi, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Database ------------------------------------------------------------------------------------
        self.db = Database()

        # Get instance
        self.formEditUi.getFirstNameInput().textChanged.connect(self.onChangeFirstNameInput)
        self.formEditUi.getLastNameInput().textChanged.connect(self.onChangeLastNameInput)
        self.formEditUi.getEmailInput().textChanged.connect(self.onChangeEmailInput)
        self.formEditUi.getDepartmentInput().textChanged.connect(self.onChangeDepartmentInput)
        self.formEditUi.getGenderInput().currentIndexChanged.connect(self.onChangeGenderInput)
        self.formEditUi.getBirthDateInput().dateChanged.connect(self.onChangeBirthDateInput)
        self.formEditUi.positionInput.textChanged.connect(self.onChangePositionInput)

        self.formEditUi.getSubmitButton().clicked.connect(self.submitUserDetail)
        self.formEditUi.getCancelButton().clicked.connect(self.closeEditPage)

        

    # Logic ------------------------------------------------------------------------------------------------

        self.userDetail = {
            'firstName' : '',
            'lastName' : '',
            'email' : '',
            'department' : '',
            'gender' : '',
            'position' : '',
            'birthDate' : QDate.currentDate().toString('dd/MM/yyyy'),
        }
        self.editUserDetail = None

    def onChangeFirstNameInput(self,text):
        self.userDetail['firstName'] = text
        # print(f"firstName: {self.firstName}")

    def onChangeLastNameInput(self,text):
        self.userDetail['lastName'] = text
        # print(f"LastName: {self.lastName}")

    def onChangeEmailInput(self,text):
        self.userDetail['email'] = text
        # print(f"Email: {self.email}")

    def onChangeDepartmentInput(self,text):
        self.userDetail['department'] = text
        # print(f"department: {self.department}")
    
    def onChangePositionInput(self,text):
        self.userDetail['position'] = text

    def onChangeGenderInput(self,index):
        # Get the current selected text
        selectedGender = self.formEditUi.getGenderInput().currentText()

        # Update the label text with the selected gender, or "None" if "Select Gender" is chosen
        if selectedGender == "Select Gender":
            self.userDetail['gender'] = ""
            # print("Selected Gender: None")
        else:
            self.userDetail['gender'] = selectedGender
            # print(f"selectedGender =  {selectedGender}")
        
        selectedGender = None

    def onChangeBirthDateInput(self,date):
        # print(f"Selected Date: {date.toString('dd/MM/yyyy')}")
        self.userDetail['birthDate'] = date.toString('dd/MM/yyyy')

    def submitUserDetail(self):

        if self.editUserDetail :
            # Update
            self.userDetail.update({'UserId':self.editUserDetail['UserId']})
            # print(self.userDetail)
            editUserStatus = self.db.editUserDetail(self.userDetail)

            if editUserStatus:
                showMessageBox(title='Edit', topic='Edit Success')  # Message Box
                self.logger.info(f"Edit User Success UserId : {self.editUserDetail['UserId']}") # Log
                self.stackedWidget.removeWidget(self.stackedWidget.widget(2))
                # Clear Data
                self.clearDataInForm()
                new_page = ControlPage(self.stackedWidget)
                self.stackedWidget.insertWidget(2,new_page)
                self.stackedWidget.setCurrentWidget(new_page)

            else:
                showMessageBox(title='Edit', topic='Edit Fail',mode='error')  # Message Box    
                self.logger.info(f"Edit User Fail UserId : {self.editUserDetail['UserId']}") # Log

        else:
            # Insert
            createUserStatus =  self.db.createUserDetail(self.userDetail) 

            if createUserStatus:
                showMessageBox(title='Insert', topic='Insert Success')  # Message Box
                self.logger.info(f"Create NewUser Success") # Log
                # Clear Data
                self.clearDataInForm()

                # Rerender ControlPage
                self.stackedWidget.removeWidget(self.stackedWidget.widget(2))
                new_page = ControlPage(self.stackedWidget)
                self.stackedWidget.insertWidget(2,new_page)
                self.stackedWidget.setCurrentWidget(new_page)

            else:
                showMessageBox(title='Insert', topic='Insert Fail',mode='error')  # Message Box 
                self.logger.info(f"Create NewUser Fail") # Log     

    
    def closeEditPage(self):
        # Clear Data
        self.clearDataInForm()

        # Rerender ControlPage
        index = self.stackedWidget.indexOf(self.stackedWidget.widget(2)) # Get the current index of ControlPage before removing it
        self.stackedWidget.removeWidget(self.stackedWidget.widget(2)) # Remove the old ControlPage
        new_page = ControlPage(self.stackedWidget) # Create a new ControlPage
        self.stackedWidget.insertWidget(index, new_page) # Insert the new ControlPage at the same index
        self.stackedWidget.setCurrentWidget(new_page) # Switch to the new ControlPage





    def populateForm(self,user_data):
        self.editUserDetail = user_data
        if user_data:
            print(user_data['Gender'])
            # print(f"Populating form with data: {user_data}")
            self.formEditUi.getSubmitButton().setText('Edit')
            # Populate the form fields with the data from user_data
            self.formEditUi.getFirstNameInput().setText(user_data['FirstName'])
            self.formEditUi.getLastNameInput().setText(user_data['LastName'])
            self.formEditUi.getEmailInput().setText(user_data['Email'])
            self.formEditUi.getDepartmentInput().setText(user_data['Department'])
            self.formEditUi.getGenderInput().setCurrentText(user_data['Gender'])
            self.formEditUi.positionInput.setText(user_data['Position'])
            self.formEditUi.getBirthDateInput().setDate(QDate.fromString(user_data['BirthDate'], "dd/MM/yyyy"))

        else:
            print('No data received')
            self.formEditUi.getSubmitButton().setText('Submit')

    # Clear Data
    def clearDataInForm(self):
        self.formEditUi.getFirstNameInput().clear()
        self.formEditUi.getLastNameInput().clear()
        self.formEditUi.getEmailInput().clear()
        self.formEditUi.getDepartmentInput().clear()
        self.formEditUi.getGenderInput().setCurrentIndex(0)  # Reset to default or first item
        self.formEditUi.positionInput.clear()
        self.formEditUi.getBirthDateInput().setDate(QDate.currentDate()) 

