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

def showMessageDeleteDialog(self):
    msgBox = QMessageBox(self)
    msgBox.setWindowTitle('Delete Accout')
    msgBox.setText('Are you sure you want to delete this item?')
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
    