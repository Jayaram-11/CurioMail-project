import sqlite3
from sqlite3 import IntegrityError

DB_NAME="Users_Data.db"

class Email_Storage:
    def __init__(self):
        pass
    def initialize_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''Create Table if not exists Emails(UID integer primary key autoincrement ,
                                Email_id text not null unique)''')
        cursor.execute("Create Table if not exists Suggestions(SNo integer primary key autoincrement, Comments text )")
        print("DB successfully created")
        conn.commit()
        conn.close()

    def add_email(self,email:str)-> bool:

        #cursor.execute("delete from sqlite_sequence where name='Email'")
        #cursor.execute("delete from Email")
        try:
            conn=sqlite3.connect(DB_NAME)
            cursor=conn.cursor()
            cursor.execute("Insert into Emails(Email_id) values(?)", (email,))
            conn.commit()
            conn.close()
            return True
        except IntegrityError:
            print(f"Email{email} already exists")
            return True
        except Exception as e:
            print(f"Error:{e}")
            return False


    def add_suggestion(self,suggestion: str) -> bool:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Suggestions(Comments) VALUES (?)", (suggestion,))
            conn.commit()
            conn.close()
            print(f"DATABASE: Successfully saved suggestion.")
            return True
        except Exception as e:
            print(f"DATABASE: An error occurred: {e}")
            return False

    def get_subscribers(self):
        try:
            conn=sqlite3.connect(DB_NAME)
            cursor=conn.cursor()
            cursor.execute("Select Email_id from Emails")
            emails=[row[0] for row in cursor.fetchall()]
            return emails
        except Exception as e:
            print(f"Error occurred: {e}")


