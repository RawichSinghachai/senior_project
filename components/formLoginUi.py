from PyQt6.QtCore import Qt , QSize
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import ( QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy)

class FormLoginUi(QWidget):
    def __init__(self):
        super().__init__()

        vBoxForm = QVBoxLayout()
        vBoxForm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBoxForm)

        # Form Login
        # Grop UserName------------------------------------------------------------------------
        vBoxGroupUsername = QVBoxLayout()
        vBoxForm.addLayout(vBoxGroupUsername)


        # User Lable
        self.userLableInput = QLabel('UserName')
        self.userLableInput.setFixedWidth(120)
        self.userLableInput.setStyleSheet(
            """
                font-size: 20px;
                font-weight: bold;
            """
        )
        vBoxGroupUsername.addWidget(self.userLableInput)


        # User Input
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
        self.userInput.setFixedSize(QSize(300,40))
        vBoxGroupUsername.addWidget(self.userInput)

        # Vertical Spacer
        vertical_spacer = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        vBoxForm.addItem(vertical_spacer)


        # Grop UserName------------------------------------------------------------------------
        vBoxGroupPassword = QVBoxLayout()
        vBoxForm.addLayout(vBoxGroupPassword)
        
        # Password Lable
        self.passwordLableInput = QLabel('Password')
        self.passwordLableInput.setFixedWidth(120)
        self.passwordLableInput.setStyleSheet(
            """
                font-size: 20px;
                font-weight: bold;
            """
        )
        vBoxGroupPassword.addWidget(self.passwordLableInput)

        # Vertical Spacer
        vertical_spacer = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        vBoxForm.addItem(vertical_spacer)

        # Password Input
        self.passwordInput = QLineEdit()
        self.passwordInput.setPlaceholderText('Fill Password')
        self.passwordInput.setFixedSize(QSize(300,40))
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


        # Button Submit
        self.signUpBtn = QPushButton('LogIn')
        self.signUpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
        self.lableToCreateAccountPage = QLabel('Register')

        self.lableToCreateAccountPage.setStyleSheet(
            '''
                font-size:10px;
                font-weight: bold;
                color:#004aad;
            '''
        )
        hBoxSubLable.addWidget(self.lableToCreateAccountPage)

        # # Text Sub Lable |
        # self.line = QLabel('|')
        # self.line.setStyleSheet(
        #     '''
        #         font-size:10px;
        #         font-weight: bold;
        #         color:#004aad;
        #     '''
        # )
        # hBoxSubLable.addWidget(self.line)

        # self.lableToPageForgetPassword = QLabel('Forget Password')
        # self.lableToPageForgetPassword.setStyleSheet(
        #     '''
        #         font-size:10px;
        #         font-weight: bold;
        #         color:#004aad;
        #     '''
        # )
        # hBoxSubLable.addWidget(self.lableToPageForgetPassword)       
        
       
    def getSignUpBtn(self):
        return self.signUpBtn

    def getUserInput(self):
        return self.userInput

    def getPasswordInput(self):
        return self.passwordInput
    
    def getLableToCreateAccountPage(self):
        return self.lableToCreateAccountPage
