from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class CustomTableWidget(QTableWidget):
    def wheelEvent(self, event):
        """ Handle horizontal scroll when Shift is pressed """
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - event.angleDelta().y())
        else:
            super().wheelEvent(event)

class TableUi(QWidget):
    def __init__(self, listUsers):
        super().__init__()

        # Root Layout
        vBox = QVBoxLayout()
        vBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vBox)

        # Table
        self.listUsers = listUsers
        self.headers = ['FirstName', 'LastName', 'Department', 'Position', 'Email', 'Gender', 'BirthDate', 'Delete']  # Removed 'UserId'
        self.table = CustomTableWidget()
        self.table.setRowCount(len(listUsers))
        self.table.setColumnCount(len(self.headers))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Don't edit data in table

        # Set selection mode to single row selection only
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Don't expand cells
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Connect signals for row selection
        self.table.verticalHeader().sectionClicked.connect(self.selectRow)
        self.table.cellClicked.connect(self.selectRow)

        self.iconDeleteDict = {}

        # Set Header Table
        for i, h in enumerate(self.headers):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(h))

        self.loadData()

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                gridline-color: #dddddd;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #dddddd;
            }
            QHeaderView::section {
                background-color: #505558;
                color: white;
                padding: 5px;
                border: 1px solid #2e3a42;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #a8d8d8;
                color: black;
            }
        """)
        vBox.addWidget(self.table)

        self.rowData = {}
        self.selectedRowIndex = None  # Store selected row index

    def loadData(self):
        """โหลดข้อมูลใหม่เข้า Table โดยไม่แสดง UserId"""
        self.table.setRowCount(len(self.listUsers))
        self.iconDeleteDict.clear()

        for row_index, user in enumerate(self.listUsers):
            for col_index, key in enumerate(self.headers[:-1]):  # Exclude 'Delete' column
                item = QTableWidgetItem(str(user[key]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, col_index, item)

            # Add delete icon
            iconDelete = QLabel()
            iconDelete.setPixmap(QPixmap('trash.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            iconDelete.setAlignment(Qt.AlignmentFlag.AlignCenter)
            iconDelete.setStyleSheet("background-color: transparent;")

            self.table.setCellWidget(row_index, len(self.headers) - 1, iconDelete)
            self.iconDeleteDict[user["UserId"]] = iconDelete  # Keep track of UserId internally

    def selectRow(self, row, column=None):
        """ Select or deselect a row when clicking on it. """
        if row == self.selectedRowIndex:
            # If clicking the same row, deselect it
            self.table.clearSelection()
            self.rowData = {}
            self.selectedRowIndex = None
            print("Row deselected")
        else:
            # Select new row
            if 0 <= row < len(self.listUsers):
                self.rowData = self.listUsers[row]
                self.selectedRowIndex = row
                print("Selected Row Data:", self.rowData)

    def getRowData(self):
        return self.rowData
    
    def updateTable(self, listUsers):
        """ อัปเดตข้อมูลใน QTableWidget """
        self.listUsers = listUsers
        self.table.clearContents()  # เคลียร์ข้อมูลเก่าก่อน
        self.loadData()  # โหลดข้อมูลใหม่
