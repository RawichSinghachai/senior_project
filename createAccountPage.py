from PyQt6.QtCore import Qt 
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QMouseEvent

from components.formCreateAccountUi import FormCreateAccountUi
from components.imageTitle import ImageTitle
from utils.messageBox import showMessageBox
from database.database import Database

class CreateAccountPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget
        
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        # Title
        self.titleLoginLable = QLabel('Create Account')
        self.titleLoginLable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLoginLable.setStyleSheet(
            '''
                font-size:30px;
                font-weight: bold;
            '''
        )
        vBox.addWidget(self.titleLoginLable)



        # hBox LayOut
        hBoxContent = QHBoxLayout()
        hBoxContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBox.addLayout(hBoxContent)


        # Image Title
        self.imageTitle = ImageTitle('assets/tseLogo.png', 400, 400)
        hBoxContent.addWidget(self.imageTitle, alignment=Qt.AlignmentFlag.AlignCenter)


        # FormLogin UI
        self.formRegister = FormCreateAccountUi()
        hBoxContent.addWidget(self.formRegister, alignment=Qt.AlignmentFlag.AlignCenter)

        # import instance -------------------------------------------------------------------------
        
        # get EmailInput instance
        self.formRegister.getEmailInput().textChanged.connect(self.onChangeEmailInput)
        # get UserInput instance
        self.formRegister.getUserInput().textChanged.connect(self.onChangeUserInput)
        # get PawwordInput instance
        self.formRegister.getPasswordInput().textChanged.connect(self.onChangePasswordInput)

        # get signUpbtn instance
        self.formRegister.getSignUpBtn().clicked.connect(self.submitRegister)

        # Get instance of LableToLoginPage
        self.formRegister.getLableToLoginPage().mousePressEvent = self.onClickToLoginPage
        


    # DataBase ------------------------------------------------------------------------------------
        self.db = Database.getInstance()

    # event -------------------------------------------------------------------------------------
        self.adminRegister = {
            'email' : '',
            'username' : '',
            'password' : ''
        }

    def keyPressEvent(self, event):
        if self.stackedWidget.currentIndex() == 1:
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.submitRegister()

    def onClickToLoginPage(self,event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            print('Clicked Login label')
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
    
    def onChangeEmailInput(self, text):
        print(f"Email changed to: {text}")
        self.adminRegister['email'] = text

    # get username
    def onChangeUserInput(self, text):
        print(f"Username changed to: {text}")
        self.adminRegister['username'] = text

    # get password
    def onChangePasswordInput(self, text):
        print(f"Password changed to: {text}")
        self.adminRegister['password'] = text

    def clearFormInput(self):
        self.formRegister.getEmailInput().clear()
        self.formRegister.getUserInput().clear()
        self.formRegister.getPasswordInput().clear()
        self.adminRegister = {
            'email' : '',
            'username' : '',
            'password' : ''
        }

    # Submit Register
    def submitRegister(self):
        # write register in Sqlite
        resigterStatus = self.db.register(self.adminRegister)
        if resigterStatus:
            showMessageBox(title='Register',topic='Register Success') # Message Box
            self.clearFormInput()
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        else:
            showMessageBox(title='Register', topic='Register Failed', mode=('error'))
        print(f"Email  : {self.adminRegister['email']}   username : {self.adminRegister['username']} password : {self.adminRegister['password']}")

