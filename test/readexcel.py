import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
import pandas as pd

class ExcelReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Reader")
        self.setGeometry(300, 200, 500, 300)
        
        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Button to open file dialog
        self.open_button = QPushButton("Open Excel File")
        self.open_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.open_button)
        
        # Label to show selected file and content
        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)
        
        self.content_label = QLabel("")
        self.content_label.setWordWrap(True)
        layout.addWidget(self.content_label)
        
    def open_file_dialog(self):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Excel File", 
            "", 
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if file_path:
            self.file_label.setText(f"Selected File: {file_path}")
            self.read_excel(file_path)
        else:
            self.file_label.setText("No file selected")
    
    def read_excel(self, file_path):
        try:
            # Read Excel file using pandas
            df = pd.read_excel(file_path)
            print(len(df.to_dict(orient="records")))
            
            # Show the first few rows
            preview = df.to_string(index=False)
            self.content_label.setText(f"File Content Preview:\n{preview}")
        except Exception as e:
            self.content_label.setText(f"Error reading file:\n{e}")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelReaderApp()
    window.show()
    sys.exit(app.exec())
