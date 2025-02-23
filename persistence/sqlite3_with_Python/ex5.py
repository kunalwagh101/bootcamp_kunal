"""
Reading Data: Implement a function to fetch and print all records from the products table.
The function should query all records and print them out.
"""


import sqlite3 

def connect_db(price,id):
    connection =  sqlite3.connect('store.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE products set price = ? WHERE id =? ",(price,id) )
    print( f"Price value as changed to {price}")


    connection.commit()
    connection.close()  
   

if __name__ == "__main__":
    connect_db(100,1)
