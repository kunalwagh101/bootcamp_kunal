"""

No.7
Using a Class: Create a Product class to handle SQLite operations for the products table.
The class should include methods for adding, updating, deleting, and listing products..
"""


import sqlite3 

import sqlite3

class Product:
    def __init__(self, db_name='store.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """Create the products table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()
    
    def add_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.conn.commit()
        print(f"Product '{name}' added successfully.")
    
    def update_product(self, product_id, new_price):
        self.cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            print(f"No product found with id {product_id}.")
        else:
            print(f"Product with id {product_id} updated to new price {new_price}.")
    
    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()
        print(f"Product with id {product_id} deleted successfully.")
    
    def list_products(self):
    
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No products found.")
    
    def __del__(self):
        self.conn.close()


if __name__ == "__main__":

    product_manager = Product()
    product_manager.add_product("a1", 50)
    print("Listing all products:")
    product_manager.list_products() 
    product_manager.update_product(1, 100)
    product_manager.delete_product(1)
    print("Products after deletion:")
    product_manager.list_products()
