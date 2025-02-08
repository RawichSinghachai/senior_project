from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import (QCoreApplication, Qt , QSize,QTimer, QDateTime,QDate)
from PyQt6.QtGui import (QColor)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QPushButton, QVBoxLayout 
    ,QGridLayout,QLineEdit,QMessageBox,QGroupBox,QSpacerItem,QTableWidget
    ,QTableWidgetItem,QHeaderView)
from PyQt6.QtGui import QMouseEvent




class ProcessPage(QWidget):
    def __init__(self,stackedWidget):
        super().__init__()


        self.stackedWidget = stackedWidget

        self.setFixedSize(QSize(800, 500))
        self.setStyleSheet("background-color: #B4B4B4;")

        self.user_data = {
            'firstName' : '',
            'lastName' : '',
            'email' : '',
            'department' : '',
            'gender' : '',
            'birthDate' : QDate.currentDate().toString('dd/MM/yyyy')
        }
        self.user_data = None

        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)


        self.title = QLabel('Detail User')
        self.title.setStyleSheet(
            """
                font-size: 30px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.title,alignment=Qt.AlignmentFlag.AlignCenter)


        self.message = QLabel('IsLoading.....')
        self.message.setStyleSheet(
            """
                font-size: 50px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.message,alignment=Qt.AlignmentFlag.AlignCenter)

        self.area = QLabel('Area ....')
        self.area.setStyleSheet(
            """
                font-size: 12px;
                font-weight: bold;
            """
        )
        vBox.addWidget(self.area)


        self.backBtn = QPushButton('Back')
        self.backBtn.setStyleSheet('''
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
        vBox.addWidget(self.backBtn)


        self.backBtn.clicked.connect(self.backPage)


    def backPage(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(2))



    def setUser(self, user_data):
        if user_data:
            self.user_data = user_data


    def loading_success(self,data):
        self.area.setText(str(data))
        print("Current stackedWidget:", self.stackedWidget.currentIndex())
        print(f"show arew {data}")

        
    def setTextMessage(self,message):
        self.message.setText(message)

# if __name__ == "__main__":
#     app = QCoreApplication.instance()
#     if app is None:
#         app = QApplication([])

#     window = ProcessPage()
#     window.show()
#     app.exec()