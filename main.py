import mediapipe
from PyQt6.QtCore import (QCoreApplication, Qt , QSize)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget)
from PyQt6.QtGui import QIcon, QMouseEvent, QFontDatabase, QFont

from components.formLoginUi import FormLoginUi
from components.imageTitle import ImageTitle
from utils.messageBox import showMessageBox, handleCloseEvent
from database.database import Database
from createAccountPage import CreateAccountPage
from controlPage import ControlPage

from editPage import EditPage
from detailPage import DetailPage
from processPage import ProcessPage
from utils.logger import AppLogger



class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Hygiene Testing")
        self.setWindowIcon(QIcon("assets/tseLogo.png"))
        self.setFixedSize(QSize(1600, 900))
        # self.setFixedSize(QSize(1024, 768))
        self.setStyleSheet("background-color: #B4B4B4;")

        # StepUp Logger
        self.logger = AppLogger.get_logger()
        
        # Root Layout
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        # LoginPage Widget
        self.loginPageWidget = QWidget()
        loginPageVBox = QVBoxLayout()
        loginPageVBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loginPageWidget.setLayout(loginPageVBox)

        # Title
        self.titleLoginLabel = QLabel('Hand Hygiene Testing')
        self.titleLoginLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.titleLoginLabel.setStyleSheet(
            '''
                font-size: 30px;
                font-weight: bold;
            '''
        )
        loginPageVBox.addWidget(self.titleLoginLabel)

        # Center layout
        hBoxCenter = QHBoxLayout()
        hBoxCenter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loginPageVBox.addLayout(hBoxCenter)

        # Image Title
        self.imageTitle = ImageTitle('assets/tseLogo.png', 400, 400)
        hBoxCenter.addWidget(self.imageTitle, alignment=Qt.AlignmentFlag.AlignCenter)

        # FormLogin UI
        self.formLogin = FormLoginUi()
        hBoxCenter.addWidget(self.formLogin, alignment=Qt.AlignmentFlag.AlignCenter)

        # Stack Widget ----------------------------------------------------------------------------------
        self.stackedWidget = QStackedWidget()
         # Add LoginPage and CreateAccountPage to QStackedWidget
        self.stackedWidget.addWidget(self.loginPageWidget)

        # Create Account Page
        self.createAccountPage = CreateAccountPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.createAccountPage)

        # Control Page
        self.controlPage = ControlPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.controlPage)

        # Edit Page
        self.editPage = EditPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.editPage)

        # Detail Page
        self.detailPage = DetailPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.detailPage)

        # progress Page
        self.processPage = ProcessPage(self.stackedWidget)
        self.stackedWidget.addWidget(self.processPage)


        vBox.addWidget(self.stackedWidget)

        # ------------------------------------------------------------------------------------------

        # Logic --------------------------------------------------------------------------------------

        # Get UserInput instance
        self.formLogin.getUserInput().textChanged.connect(self.onUserInputChanged)
        # Get PasswordInput instance
        self.formLogin.getPasswordInput().textChanged.connect(self.onPasswordInputChanged)

        # Get signUpBtn instance
        self.formLogin.getSignUpBtn().clicked.connect(self.submitLogin)

        # Get instance of LableToPageRegister
        self.formLogin.getLableToCreateAccountPage().mousePressEvent = self.onClickToCreateAccount

    # Database ------------------------------------------------------------------------------------
        self.db = Database.getInstance()
        

    # Event -------------------------------------------------------------------------------------
        self.adminLogin = {
            'username' : '',
            'password' : ''
        }
        

    # Keyboard Event 
    def keyPressEvent(self, event):
        if self.stackedWidget.currentIndex() == 0:
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                self.submitLogin()


    def onClickToCreateAccount(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clearFormInput()
            self.stackedWidget.setCurrentWidget(self.createAccountPage)  # Switch to CreateAccountPage

    # Get username
    def onUserInputChanged(self, text):
        self.adminLogin['username'] = text

    # Get password
    def onPasswordInputChanged(self, text):
        self.adminLogin['password'] = text
    
    def clearFormInput(self):
        self.formLogin.getUserInput().clear()
        self.formLogin.getPasswordInput().clear()
        self.adminLogin = {
            'username' : '',
            'password' : ''
        }

    # Submit Login
    def submitLogin(self):
        # Check Login in SQLite; return True when login is successful
        loginStatus = self.db.checkLogin(self.adminLogin)

        if loginStatus:
            showMessageBox(title='Login', topic='Login Success')  # Message Box
            self.clearFormInput()
            self.stackedWidget.setCurrentWidget(self.controlPage) 
            self.logger.info(f"Login Success username : {self.adminLogin['username']}") # Log
        
        else:
            showMessageBox(title='Login', topic='Login Fail',mode='error')  # Message Box
            self.logger.info(f"Login Unsuccess username : {self.adminLogin['username']}") # Log

    def closeEvent(self, event):
        handleCloseEvent(self, event, self.db)

 
    

if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])

    font_id = QFontDatabase.addApplicationFont("font/NotoSans-Regular.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
        app.setFont(QFont(font_families[0])) 
    else:
        app.setFont(QFont("Arial"))  

    window = LoginPage()
    window.show()
    app.exec()