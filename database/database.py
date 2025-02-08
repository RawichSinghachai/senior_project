from PyQt6.QtSql import QSqlDatabase, QSqlQuery

import uuid
from datetime import datetime

class Database:
    def __init__(self):
        # Ensure we use a unique connection name, e.g., "mainConnection"
        if QSqlDatabase.contains("mainConnection"):
            self.db = QSqlDatabase.database("mainConnection")
        else:
            self.db = QSqlDatabase.addDatabase('QSQLITE', "mainConnection")
            self.db.setDatabaseName('database/db.sqlite')
            if not self.db.open():
                raise Exception("Failed to open the database")

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
        sql = 'INSERT INTO Admin (Email, Username, Password) VALUES (?, ?, ?);'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(adminRegister['email'])
        query.addBindValue(adminRegister['username'])
        query.addBindValue(adminRegister['password'])
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
                u.FirstName, u.LastName, u.Department, u.Position, u.Email, u.Gender, u.BirthDate,
                COALESCE(utr.LeftScoreFront, 0), COALESCE(utr.LeftScoreBack, 0),
                COALESCE(utr.RightScoreFront, 0), COALESCE(utr.RightScoreBack, 0),
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
                    'FirstName': query.value(0),
                    'LastName': query.value(1),
                    'Department': query.value(2),
                    'Position': query.value(3),
                    'Email': query.value(4),
                    'Gender': query.value(5),
                    'BirthDate': query.value(6),
                    'LeftScoreFront': query.value(7),
                    'LeftScoreBack': query.value(8),
                    'RightScoreFront': query.value(9),
                    'RightScoreBack': query.value(10),
                    'TotalScore': query.value(11),
                    'TestingDate': query.value(12),
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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'''
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
        
    def creatUserTesting(self,userId,data):
        # สร้าง ProfileId (UUID)
        profile_id = str(uuid.uuid4())
        testing_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # SQL Query
        sql = '''
        INSERT INTO UserTestResult (ProfileId, UserId, LeftScoreFront, LeftScoreBack, 
                                    RightScoreFront, RightScoreBack, TotalScore, TestingDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        
        # Execute Query
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(profile_id)
        query.addBindValue(userId)
        query.addBindValue(data['LeftScoreFront'])
        query.addBindValue(data['LeftScoreBack'])
        query.addBindValue(data['RightScoreFront'])
        query.addBindValue(data['RightScoreBack'])
        query.addBindValue(data['TotalScore'])
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
            utr.LeftScoreFront, utr.LeftScoreBack, 
            utr.RightScoreFront, utr.RightScoreBack, 
            utr.TotalScore, utr.TestingDate
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
                    'LeftScoreFront': query.value(7),
                    'LeftScoreBack': query.value(8),
                    'RightScoreFront': query.value(9),
                    'RightScoreBack': query.value(10),
                    'TotalScore': query.value(11),
                    'TestingDate': query.value(12),
                }
                results.append(result)
        else:
            print("Query failed:", query.lastError().text())

        return results


    def editUserDetail(self,userDetail):
        UpdateAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = '''UPDATE User SET FirstName = ? ,LastName = ?, Department = ?,
                Gender = ?, Email = ?, BirthDate = ?, UpadatedAt = ?
                WHERE UserId = ? ;'''
        
        query = QSqlQuery(self.db)
        query.prepare(sql)

        query.addBindValue(userDetail['firstName'])
        query.addBindValue(userDetail['lastName'])
        query.addBindValue(userDetail['department'])
        query.addBindValue(userDetail['gender'])
        query.addBindValue(userDetail['email'])
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


# No self.db.close() calls in individual methods; connection is managed at the class level
