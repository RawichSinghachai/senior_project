from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt 
from PyQt6.QtWidgets import ( QWidget, QLabel, QVBoxLayout )


class ImageTitle(QWidget):
    def __init__(self, path, width, height):
        super().__init__()

        self.path = path
        self.width = width
        self.height = height
        
        vBoxImage = QVBoxLayout()
        self.setLayout(vBoxImage)

        img = QPixmap(self.path)
        img = img.scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        lableImage = QLabel()
        lableImage.setPixmap(img)
        vBoxImage.addWidget(lableImage)
