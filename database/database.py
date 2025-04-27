from PyQt6.QtSql import QSqlDatabase, QSqlQuery

import os
import uuid
from datetime import datetime
from utils.handScoreCalculator import calculate_hand_score

class Database:
    _instance = None

    @staticmethod
    def getInstance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self):
        if hasattr(self, 'db'):
            return  # ป้องกันการเรียกซ้ำ
        self.db = None
        db_path = 'database/db.sqlite'
        db_dir = os.path.dirname(db_path)

        # ถ้าโฟลเดอร์ไม่มีอยู่ให้สร้างใหม่
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # ถ้าไฟล์ไม่มีอยู่ให้สร้างใหม่
        if not os.path.exists(db_path):
            open(db_path, 'w').close()


        if QSqlDatabase.contains("mainConnection"):
            self.db = QSqlDatabase.database("mainConnection")
        else:
            self.db = QSqlDatabase.addDatabase('QSQLITE', "mainConnection")
            self.db.setDatabaseName('database/db.sqlite')
            if not self.db.open():
                raise Exception("Failed to open the database")

        
        self.createAdminTable()
        self.createUserTable()
        self.createUserTestResultTable()
            
    def tableExists(self, table_name):
        """ ตรวจสอบว่าตารางมีอยู่หรือไม่ """
        query = QSqlQuery(self.db)
        query.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name = ?;")
        query.addBindValue(table_name)
        if query.exec() and query.next():
            return True
        return False    
    
    def createAdminTable(self):
        """ สร้างตาราง Admin ถ้ายังไม่มี """
        if not self.tableExists("Admin"):
            query = QSqlQuery(self.db)
            sql = """
            CREATE TABLE "Admin" (
                    "AdminId"	TEXT UNIQUE,
                    "UserName"	TEXT,
                    "Password"	TEXT,
                    "Email"	TEXT ,
                    "CreatedAt"	TEXT,
                    PRIMARY KEY("AdminId")
                );
            """
            if not query.exec(sql):
                print("Failed to create Admin table:", query.lastError().text())
            else:
                print("Table 'Admin' created successfully!")

    def createUserTable(self):
        """ สร้างตาราง User ถ้ายังไม่มี """
        if not self.tableExists("User"):
            query = QSqlQuery(self.db)
            sql = """
            CREATE TABLE "User" (
                "UserId"	TEXT UNIQUE,
                "FirstName"	TEXT,
                "LastName"	TEXT,
                "Department"	TEXT,
                "Position"	TEXT,
                "Email"	TEXT ,
                "Gender"	TEXT,
                "BirthDate"	TEXT,
                "CreatedAt"	TEXT,
                "UpdatedAt"	INTEGER,
                PRIMARY KEY("UserId")
            );
            """
            if not query.exec(sql):
                print("Failed to create User table:", query.lastError().text())
            else:
                print("Table 'User' created successfully!")

    def createUserTestResultTable(self):
        """ สร้างตาราง UserTestResult ถ้ายังไม่มี """
        if not self.tableExists("UserTestResult"):
            query = QSqlQuery(self.db)
            sql = """
            CREATE TABLE "UserTestResult" (
                "ProfileId"	TEXT,
                "UserId"	TEXT,
                "LeftHandFrontScore"	INTEGER,
                "LeftHandBackScore"	INTEGER,
                "RightHandFrontScore"	INTEGER,
                "RightHandBackScore"	INTEGER,
                "TotalScore"	INTEGER,
                "TestingDate"	TEXT,
                PRIMARY KEY("ProfileId")
            );
            """
            if not query.exec(sql):
                print("Failed to create UserTestResult table:", query.lastError().text())
            else:
                print("Table 'UserTestResult' created successfully!")

    def getAdmin(self):
        sql = 'SELECT * FROM Admin;'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return []

        admins = []
        while query.next():
            admin = {
                'id': query.value(0),           # Assuming the first column is 'id'
                'username': query.value(1),     # Assuming the second column is 'username'
                'email': query.value(2),        # Assuming the third column is 'email'
                'password': query.value(3)      # Assuming the fourth column is 'password'
            }
            admins.append(admin)
        
        self.result = admins
        return admins

    def register(self, adminRegister):

        adminId = uuid.uuid4()
        createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = 'INSERT INTO Admin (AdminId, Username, Password, Email, CreatedAt) VALUES (?, ?, ?, ?, ?);'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(str(adminId))
        query.addBindValue(adminRegister['username'])
        query.addBindValue(adminRegister['password'])
        query.addBindValue(adminRegister['email'])
        query.addBindValue(createdAt)
        result = query.exec()

        if not result:
            print("Failed to execute query:", query.lastError().text())
        return result

    def checkLogin(self, adminLogin):
        sql = '''
            SELECT COUNT(*)
            FROM Admin
            WHERE (Username = ? OR Email = ?) AND Password = ?;
        '''
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(adminLogin['username'])  # This will be used for both username and email
        query.addBindValue(adminLogin['username'])  # This will be used for both username and email
        query.addBindValue(adminLogin['password'])
        
        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return False
        
        if query.next():
            count = query.value(0)
            if count > 0:
                print("Login successful")
                return True
            else:
                print("Login failed: Incorrect username/email or password")
                return False
        else:
            print("Query did not return any results")
            return False
    
    def getAllUser(self):
        sql = 'SELECT UserId, FirstName, LastName, Department, Position , Email, Gender, BirthDate FROM User'
        query = QSqlQuery(self.db)
        query.prepare(sql)

        users = []

        if query.exec():
            # Iterate through the query results
            while query.next():
                # Build a dictionary for each row
                user = {
                    'UserId': query.value(0),
                    'FirstName': query.value(1),
                    'LastName': query.value(2),
                    'Department': query.value(3),
                    'Position': query.value(4),
                    'Email': query.value(5),
                    'Gender': query.value(6),
                    'BirthDate': query.value(7)  # Convert QDate to string
                }
                users.append(user)
        else:
            print(f"Error executing query: {query.lastError().text()}")

        return users
    # Edit if not data show null
    def getAllUserData(self):
        sql = '''
            SELECT 
                u.UserId, utr.ProfileId,u.FirstName, u.LastName, u.Department, u.Position, u.Email, u.Gender, u.BirthDate,
                COALESCE(utr.LeftHandFrontScore, 0), COALESCE(utr.LeftHandBackScore, 0),
                COALESCE(utr.RightHandFrontScore, 0), COALESCE(utr.RightHandBackScore, 0),
                COALESCE(utr.TotalScore, 0), COALESCE(utr.TestingDate, '')
            FROM User AS u
            LEFT JOIN UserTestResult AS utr ON u.UserId = utr.UserId
            ORDER BY utr.TestingDate DESC NULLS LAST;
        '''
        
        query = QSqlQuery(self.db)
        query.prepare(sql)

        users = []

        if query.exec():
            while query.next():
                user = {
                    'UserId': query.value(0),
                    'ProfileId': query.value(1),
                    'FirstName': query.value(2),
                    'LastName': query.value(3),
                    'Department': query.value(4),
                    'Position': query.value(5),
                    'Email': query.value(6),
                    'Gender': query.value(7),
                    'BirthDate': query.value(8),
                    'LeftHandFrontScore': query.value(9),
                    'LeftHandBackScore': query.value(10),
                    'RightHandFrontScore': query.value(11),
                    'RightHandBackScore': query.value(12),
                    'TotalScore': query.value(13),
                    'TestingDate': query.value(14),
                }
                users.append(user)
        else:
            print(f"Error executing query: {query.lastError().text()}")

        return users


    
    def createUserDetail(self, userDetail):

        userId = uuid.uuid4()
        createdAtandUpdateAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        
        sql = '''INSERT INTO User (UserId, FirstName, LastName, Department, Position, Email, Gender, 
                BirthDate, CreatedAt, UpdatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        query = QSqlQuery(self.db)
        query.prepare(sql)
        # add uuid
        query.addBindValue(str(userId))
        query.addBindValue(userDetail['firstName'])
        query.addBindValue(userDetail['lastName'])
        query.addBindValue(userDetail['department'])
        query.addBindValue(userDetail['position'])
        query.addBindValue(userDetail['email'])
        query.addBindValue(userDetail['gender'])
        query.addBindValue(userDetail['birthDate'])
        query.addBindValue(createdAtandUpdateAt)
        query.addBindValue(createdAtandUpdateAt)

        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return False
        else:
            return True
        
    def creatUserTesting(self,userId, profile_id, data):
        # สร้าง ProfileId (UUID)
        # profile_id = str(uuid.uuid4())
        testing_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        left_front, left_back, right_front, right_back, total = calculate_hand_score(data)

        # SQL Query
        sql = '''
        INSERT INTO UserTestResult (ProfileId, UserId, LeftHandFrontScore, LeftHandBackScore, 
                                    RightHandFrontScore, RightHandBackScore, TotalScore, TestingDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        
        # Execute Query
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(profile_id)
        query.addBindValue(userId)
        query.addBindValue(left_front)
        query.addBindValue(left_back)
        query.addBindValue(right_front)
        query.addBindValue(right_back)
        query.addBindValue(total)
        query.addBindValue(testing_date)

        if query.exec():
            print("Inserted successfully!")
        else:
            print(f"Failed to insert: {query.lastError().text()}")
        


    def getUserData(self, UserId):
        sql = '''
        SELECT 
            u.FirstName, u.LastName, u.Department, u.Position, 
            u.Email, u.Gender, u.BirthDate, 
            utr.LeftHandFrontScore, utr.LeftHandBackScore, 
            utr.RightHandFrontScore, utr.RightHandBackScore, 
            utr.TotalScore, utr.TestingDate, utr.ProfileId
        FROM User AS u
        INNER JOIN UserTestResult AS utr ON utr.UserId = u.UserId
        WHERE u.UserId = ?
        ORDER BY utr.TestingDate DESC;
        '''

        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(UserId)

        results = []
        if query.exec():
            while query.next():
                result = {
                    'FirstName': query.value(0),
                    'LastName': query.value(1),
                    'Department': query.value(2),
                    'Position': query.value(3),
                    'Email': query.value(4),
                    'Gender': query.value(5),
                    'BirthDate': query.value(6),
                    'LeftHandFrontScore': query.value(7),
                    'LeftHandBackScore': query.value(8),
                    'RightHandFrontScore': query.value(9),
                    'RightHandBackScore': query.value(10),
                    'TotalScore': query.value(11),
                    'TestingDate': query.value(12),
                    'ProfileId': query.value(13)
                }
                results.append(result)
        else:
            print("Query failed:", query.lastError().text())

        return results


    def editUserDetail(self,userDetail):
        UpdateAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(userDetail)

        sql = '''UPDATE User SET FirstName = ? ,LastName = ?, Department = ?,
                Position = ?, Email = ?, Gender = ?, BirthDate = ?, UpdatedAt = ?
                WHERE UserId = ? ;'''
        
        query = QSqlQuery(self.db)
        query.prepare(sql)

        query.addBindValue(userDetail['firstName'])
        query.addBindValue(userDetail['lastName'])
        query.addBindValue(userDetail['department'])
        query.addBindValue(userDetail['position'])
        query.addBindValue(userDetail['email'])
        query.addBindValue(userDetail['gender'])
        query.addBindValue(userDetail['birthDate'])
        query.addBindValue(UpdateAt)
        query.addBindValue(userDetail['UserId'])

        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return False
        else:
            return True
        
    def deleteUser(self,UserId):
        sql = 'DELETE FROM User WHERE UserID = ?;'
        
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(UserId)
        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return False
        else:
            return True
    
    def deleteUserTestResult(self,ProfileId):
        sql = 'DELETE FROM UserTestResult WHERE ProfileId = ?;'

        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(ProfileId)
        if not query.exec():
            print("Failed to execute query:", query.lastError().text())
            return False
        else:
            return True

    # Edit
    def import_users(self, users):

        for user in users:
            first_name = user.get('FirstName')
            last_name = user.get('LastName')
            department = user.get('Department', '')
            position = user.get('Position', '')
            email = user.get('Email', None)
            gender = user.get('Gender', '')
            birth_date = user.get('BirthDate', '')

            # เช็คว่ามีชื่อ-นามสกุลนี้อยู่แล้วหรือไม่
            check_sql = '''
            SELECT COUNT(*) FROM User WHERE FirstName = ? AND LastName = ?;
            '''
            check_query = QSqlQuery(self.db)
            check_query.prepare(check_sql)
            check_query.addBindValue(first_name)
            check_query.addBindValue(last_name)

            if not check_query.exec():
                print("Failed to execute check query:", check_query.lastError().text())
                continue

            check_query.next()
            if check_query.value(0) > 0:
                print(f"Skipping {first_name} {last_name}, already exists.")
                continue  # ข้ามไปยัง user คนถัดไป

            # เพิ่มข้อมูลใหม่
            insert_sql = '''
            INSERT INTO User (UserId, FirstName, LastName, Department, Position, Email, Gender, BirthDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            '''
            insert_query = QSqlQuery(self.db)
            insert_query.prepare(insert_sql)

            # ใช้ UUID เป็น Primary Key
   
            user_id = str(uuid.uuid4())

            insert_query.addBindValue(user_id)
            insert_query.addBindValue(first_name)
            insert_query.addBindValue(last_name)
            insert_query.addBindValue(department)
            insert_query.addBindValue(position)
            insert_query.addBindValue(email)
            insert_query.addBindValue(gender)
            insert_query.addBindValue(birth_date)

            if not insert_query.exec():
                print("Failed to insert:", insert_query.lastError().text())
            else:
                print(f"Inserted {first_name} {last_name} successfully.")

    

    def searchUser(self, search, filter = "FirstName"):
        sql = f'''SELECT UserId, FirstName, LastName, Department, Position, Email, Gender, BirthDate 
                FROM User 
                WHERE {filter} LIKE :search
            '''
        
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.bindValue(":search", f"%{search}%")  

        users = []

        if query.exec():
            while query.next():
                user = {
                    'UserId': query.value(0),
                    'FirstName': query.value(1),
                    'LastName': query.value(2),
                    'Department': query.value(3),
                    'Position': query.value(4),
                    'Email': query.value(5),
                    'Gender': query.value(6),
                    'BirthDate': query.value(7)
                }
                users.append(user)
        else:
            print(f"Error executing query: {query.lastError().text()}")

        return users
    
    def deleteAllUser(self):
    
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM UserTestResult")
        if not query.exec():
            print("Error deleting UserTestResult:", query.lastError().text())
            return False
        
        query.prepare("DELETE FROM User")
        if not query.exec():
            print("Error deleting User:", query.lastError().text())
            return False
        return True

 

    def closeDatabase(self):
        if self.db.isOpen():
            self.db.close()

        # ตรวจสอบให้แน่ใจว่าไม่มี instance อื่นใช้งาน
        connection_name = self.db.connectionName()  # ดึงชื่อ connection
        
        # ลบตัวแปรฐานข้อมูล
        del self.db  

        # ตรวจสอบว่ามี connection ที่ต้องปิดหรือไม่
        if QSqlDatabase.contains(connection_name):
            QSqlDatabase.removeDatabase(connection_name)  

            

    




