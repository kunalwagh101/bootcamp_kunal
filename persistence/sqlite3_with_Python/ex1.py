
"""
No.1 Setting Up SQLite Database: Create a SQLite database named store.db.
Write a script to connect to store.db and create it if it doesn't exist.
"""
import sqlite3 

def connect_db():
    connection =  sqlite3.connect('store.db')
    print("Done")
    connection.close()

if __name__ == "__main__":
    print(f"Created database name store.db \n")
    connect_db()
