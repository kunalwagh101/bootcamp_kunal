"""

No.6
Deleting Data: Write a function to delete a product from the table by its id.
The function should take id as a parameter and remove the corresponding record.
"""


import sqlite3 

def connect_db(id):
    connection =  sqlite3.connect('store.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?",(id,) )

    connection.commit()
    connection.close()  

    if cursor.rowcount == 0:
        print(f"No product found with id {id}.")
    else:
        print(f"Product with id {id} deleted successfully.")
    

if __name__ == "__main__":
    connect_db(1)
