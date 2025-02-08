import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget

class FileDialogExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(300, 200, 400, 200)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Button to open file dialog
        self.open_file_button = QPushButton("Open File")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.open_file_button)

        # Label to show selected file
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

    def open_file_dialog(self):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "C:/Users/Rawich/Downloads",
            "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )

        if file_path:
            self.file_label.setText(f"Selected File: {file_path}")
        else:
            self.file_label.setText("No file selected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDialogExample()
    window.show()
    sys.exit(app.exec())
