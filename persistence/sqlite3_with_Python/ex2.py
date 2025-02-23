"""
Creating a Table: Create a table products with columns for id, name, and price.
Use a SQL script to create this table in the store.db database.
"""


import sqlite3 

def connect_db():
    connection =  sqlite3.connect('store.db')
    cursor = connection.cursor()

    cursor.execute(

        '''
    CREATE TABLE IF NOT EXISTS products (
       
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL  ,
    price INTEGER NOT NULL 
    

    );

'''
    )
    connection.commit()
    connection.close()

if __name__ == "__main__":
    print(f"Created new table named products in database")
    connect_db()
