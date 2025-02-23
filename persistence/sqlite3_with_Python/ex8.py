"""
No.8
Handling Exceptions: Implement exception handling in the Product class for database operations.
Add try-except blocks to handle common SQLite errors like operational errors.
"""


import sqlite3

class Product:
    def __init__(self, db_name='store.db'):
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print("Error creating table:", e)

    def add_product(self, name, price):
        try:
            self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            self.conn.commit()
            print(f"Product '{name}' added successfully.")
        except sqlite3.Error as e:
            print("Error adding product:", e)

    def update_product(self, product_id, new_price):
        try:
            self.cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print(f"No product found with id {product_id}.")
            else:
                print(f"Product with id {product_id} updated to new price {new_price}.")
        except sqlite3.Error as e:
            print("Error updating product:", e)

    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print(f"No product found with id {product_id}.")
            else:
                print(f"Product with id {product_id} deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting product:", e)

    def list_products(self):
        try:
            self.cursor.execute("SELECT * FROM products")
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No products found.")
        except sqlite3.Error as e:
            print("Error fetching products:", e)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    product_manager = Product()
    product_manager.add_product("a1", 50)
    product_manager.list_products()
    product_manager.update_product(1, 100)
    product_manager.delete_product(1)
    product_manager.list_products()
