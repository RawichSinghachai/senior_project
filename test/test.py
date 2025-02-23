import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase

class Database:
    def __init__(self):
        # ตรวจสอบว่ามี QApplication แล้วหรือไม่
        if not QApplication.instance():
            self.app = QApplication(sys.argv)  # สร้าง QApplication ถ้ายังไม่มี
        
        connection_name = "mainConnection"
        if QSqlDatabase.contains(connection_name):
            self.db = QSqlDatabase.database(connection_name)
        else:
            self.db = QSqlDatabase.addDatabase('QSQLITE', connection_name)
            self.db.setDatabaseName('database/db.sqlite')
            if not self.db.open():
                raise Exception("Failed to open the database")

        print("Connected with name:", self.db.connectionName())

# เรียกใช้งาน Database
db = Database()
