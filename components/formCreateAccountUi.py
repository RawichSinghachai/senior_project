from PyQt6.QtCore import QCoreApplication, Qt , QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,QPushButton, QVBoxLayout \
    ,QHBoxLayout,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSizePolicy,QSpacerItem

class FormRegisterUi(QWidget):
    def __init__(self):
        super().__init__()

        vBoxForm = QVBoxLayout()
        vBoxForm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBoxForm)
        # self.setStyleSheet("background-color: #FCFCFC;")


        # Form Register
        hBoxFormFirstRow = QHBoxLayout()
        vBoxForm.addLayout(hBoxFormFirstRow)




        # Grop UserName ------------------------------------------------------------------------
        vBoxGroupUserName = QVBoxLayout()
        hBoxFormFirstRow.addLayout(vBoxGroupUserName)

        # Username Lable
        self.userLable = QLabel('Username  : ')
        self.userLable.setFixedWidth(120)
        self.userLable.setStyleSheet(
            """
                font-size: 16px;
                font-weight: bold;
            """
        )
        vBoxGroupUserName.addWidget(self.userLable)

        # Username Input
        self.userInput = QLineEdit()
        self.userInput.setStyleSheet(
            """
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                font-size : 15px;
            """
        )
        self.userInput.setPlaceholderText('Fill Username')
        self.userInput.setFixedSize(QSize(200,40))
        vBoxGroupUserName.addWidget(self.userInput)

        # Grop Email ------------------------------------------------------------------------
        vBoxGroupEmail = QVBoxLayout()
        hBoxFormFirstRow.addLayout(vBoxGroupEmail)

        # Email Lable
        self.emailLable = QLabel('Email  : ')
        self.emailLable.setFixedWidth(120)
        self.emailLable.setStyleSheet(
            """
                font-size: 16px;
                font-weight: bold;
            """
        )
        vBoxGroupEmail.addWidget(self.emailLable)

        # Email Input
        self.emailInput = QLineEdit()
        self.emailInput.setStyleSheet(
            """
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                font-size : 15px;
            """
        )
        self.emailInput.setPlaceholderText('Fill Email')
        self.emailInput.setFixedSize(QSize(200,40))
        vBoxGroupEmail.addWidget(self.emailInput)

        # Grop Password ------------------------------------------------------------------------
        vBoxGroupPassword = QVBoxLayout()
        vBoxForm.addLayout(vBoxGroupPassword)


        # Password Lable 
        self.passwordLable = QLabel('Password    : ')
        self.passwordLable.setFixedWidth(120)
        self.passwordLable.setStyleSheet(
            """
                font-size: 16px;
                font-weight: bold;
            """
        )
        vBoxGroupPassword.addWidget(self.passwordLable)

        # Password Input
        self.passwordInput = QLineEdit()
        self.passwordInput.setPlaceholderText('Fill Password')
        self.passwordInput.setFixedSize(QSize(200,40))
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordInput.setStyleSheet(
            """
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                font-size : 15px;
            """
        )
        vBoxGroupPassword.addWidget(self.passwordInput)


        # Spacer Item
        # spacer = QSpacerItem(0, 20)
        # vBoxForm.addSpacerItem(spacer)
        # gridForm.setRowStretch(2, 1)
        
        # Button Submit
        self.signUpBtn = QPushButton('Sign Up')
        self.signUpBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signUpBtn.setStyleSheet('''
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
        vBoxForm.addWidget(self.signUpBtn)

        # Sub Lable
        hBoxSubLable = QHBoxLayout()
        hBoxSubLable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBoxForm.addLayout(hBoxSubLable)

        # Text SubLable Register
        self.lableToLoginPage = QLabel('Login')

        self.lableToLoginPage.setStyleSheet(
            '''
                font-size:10px;
                font-weight: bold;
                color:#004aad;
            '''
        )
        # hBoxSubLable.addWidget(self.lableToLoginPage)
        hBoxSubLable.addWidget(self.lableToLoginPage)


 

   
    def getEmailInput(self):
        return self.emailInput

    def getUserInput(self):
        return self.userInput

    def getPasswordInput(self):
        return self.passwordInput
    
    def getSignUpBtn(self):
        return  self.signUpBtn
    
    def getLableToLoginPage(self):
        return self.lableToLoginPage
