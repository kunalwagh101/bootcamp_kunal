"""
Inserting Data: Write a function to insert a new product into the products table.
The function should take name and price as parameters and insert them into the table.
"""


import sqlite3 

def connect_db(name,price):
    connection =  sqlite3.connect('store.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO products (name , price) VALUES(? ,?)",(name,price) )

    print(f'Inserted new values in products database {name} ,{price}')
    connection.commit()
    connection.close()  
   

if __name__ == "__main__":
    
    connect_db("a",50)
