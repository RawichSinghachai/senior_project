from PyQt6.QtWidgets import QMessageBox


def showMessageBox(title,topic,mode='info'):
    
    if(mode == 'info'):
        icon = QMessageBox.Icon.Information
    elif(mode == 'warn'):
        icon = QMessageBox.Icon.Warning
    elif(mode == 'error'):
        icon = QMessageBox.Icon.Critical

    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(topic)
    msgBox.setIcon(icon)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgBox.exec()

def showMessageDeleteDialog(self, Title='Delete Account', meassage='Are you sure you want to delete this item?'):
    msgBox = QMessageBox(self)
    msgBox.setWindowTitle(Title)
    msgBox.setText(meassage)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    msgBox.setStyleSheet("""
        QMessageBox {
                background-color: #ffffff;         
            }
        QLabel {
                background-color: transparent;
            }
        QPushButton {
                background-color: #ffffff;
            }
        """)
    response = msgBox.exec()
    return response  
    
def handleCloseEvent(parent, event, db):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("Exit Confirmation")
    msg_box.setText("Are you sure you want to exit?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.No)

    # ✅ กำหนด CSS ให้กับ QMessageBox
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;  /* เปลี่ยนสีพื้นหลัง */
            color: black;  /* เปลี่ยนสีตัวอักษร */
            font-size: 16px;
        }
        QPushButton {
            background-color: #ffffff;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #ffffff;
        }
        QPushButton:pressed {
            background-color: #ffffff;
        }
        QLabel {
            background-color: transparent;
        }
    """)

    reply = msg_box.exec()

    if reply == QMessageBox.StandardButton.Yes:
        # print("Program is closing...")
        db.closeDatabase()
        event.accept()
    else:
        event.ignore()