"""
Reading Data: Implement a function to fetch and print all records from the products table.
The function should query all records and print them out.
"""


import sqlite3 

def connect_db():
    connection =  sqlite3.connect('store.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products " )

    read_value =  cursor.fetchall()
    for rows in read_value :
        print(rows)
    connection.close()  

    if cursor.rowcount == 0:
        print(f"No product found.")
    else:
        print(f"Printed all of the rows in table")
    

   

if __name__ == "__main__":
  
    connect_db()
