from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt 
from PyQt6.QtWidgets import ( QWidget, QLabel, QVBoxLayout )


class ImageTitle(QWidget):
    def __init__(self):
        super().__init__()
        
        vBoxForm = QVBoxLayout()
        self.setLayout(vBoxForm)

        img = QPixmap('assets/qoogle.png')
        img = img.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        lableImage = QLabel()
        lableImage.setPixmap(img)
        vBoxForm.addWidget(lableImage)
