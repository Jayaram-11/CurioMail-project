import sqlite3
from sqlite3 import IntegrityError
import psycopg2
from config import DATABASE_URL
DB_NAME="Users_Data.db"

class Email_Storage:
    def get_connection(self):
        #Establish connection to postgre sql db
        return psycopg2.connect(DATABASE_URL)

    def initialize_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Email (
                        UID SERIAL PRIMARY KEY,
                        Email_id TEXT NOT NULL UNIQUE
                    )
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Suggestions (
                        SNo SERIAL PRIMARY KEY,
                        Comments TEXT
                    )
                ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL database and tables initialized successfully.")

    def add_email(self,email:str)-> bool:

        #cursor.execute("delete from sqlite_sequence where name='Email'")
        #cursor.execute("delete from Email")
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Email (Email_id) VALUES (%s)", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"DATABASE: Successfully saved email: {email}")
            return True
        except psycopg2.IntegrityError:
            print(f"DATABASE: Email {email} already exists.")
            return True
        except Exception as e:
            print(f"DATABASE ERROR: Could not save email. Error: {e}")
            return False


    def add_suggestion(self,suggestion: str) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Suggestions (Comments) VALUES (%s)", (suggestion,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"DATABASE: Successfully saved suggestion.")
            return True
        except Exception as e:
            print(f"DATABASE ERROR: Could not save suggestion. Error: {e}")
            return False

    def get_subscribers(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Email_id FROM Email")
            subscribers = [item[0] for item in cursor.fetchall()]
            cursor.close()
            conn.close()
            return subscribers
        except Exception as e:
            print(f"DATABASE ERROR: Could not retrieve subscribers. Error: {e}")
            return []

    def remove_email(self, email: str) -> bool:

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Email WHERE Email_id = %s", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"DATABASE: Successfully removed email: {email}")
            return True
        except Exception as e:
            print(f"DATABASE ERROR: Could not remove email {email}. Error: {e}")
            return False

