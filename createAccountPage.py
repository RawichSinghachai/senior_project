from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, Qt , QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,QPushButton, QVBoxLayout \
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from components.formCreateAccountUi import FormRegisterUi
from components.imageTitle import ImageTitle
from utils.messageBox import showMessageBox
from database.database import Database

class CreateAccountPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()

        self.stackedWidget = stackedWidget
        self.setWindowTitle("Register")

        # self.setFixedSize(QSize(800,500))
        self.setStyleSheet("background-color: #B4B4B4;")
        
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(vBox)

        # Title
        self.titleLoginLable = QLabel('Create Account')
        self.titleLoginLable.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.titleLoginLable.setStyleSheet(
            '''
                font-size:30px;
                font-weight: bold;
                margin-right:120px;
                margin-top:40px;
            '''
        )
        vBox.addWidget(self.titleLoginLable)



        # hBox LayOut
        hBoxContent = QHBoxLayout()
        hBoxContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBox.addLayout(hBoxContent)


        # Image Title
        self.imageTitle = ImageTitle('assets/qoogle.png', 400, 400)
        hBoxContent.addWidget(self.imageTitle)


        # FormLogin UI
        self.formRegister = FormRegisterUi()
        hBoxContent.addWidget(self.formRegister)

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
        self.db = Database()

    # event -------------------------------------------------------------------------------------
        self.adminRegister = {
            'email' : '',
            'username' : '',
            'password' : ''
        }

    # get email
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

    # Submit Register
    def submitRegister(self):
        # write register in Sqlite
        resigterStatus = self.db.register(self.adminRegister)
        if resigterStatus:
            showMessageBox(title='Register',topic='Register Success') # Message Box
        print(f"Email  : {self.adminRegister['email']}   username : {self.adminRegister['username']} password : {self.adminRegister['password']}")

        

# app = QCoreApplication.instance()
# if app is None: app = QApplication([])


# window = CreateAccountPage()
# window.show()
# app.exec()