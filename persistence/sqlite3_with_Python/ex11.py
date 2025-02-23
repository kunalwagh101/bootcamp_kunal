"""
NO.11
Using Transactions: Modify the Product class to use transactions.
Wrap database operations in transactions to ensure data integrity.
"""
import sqlite3

class Product:
    def __init__(self, db_name='store.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_product(self, name, price):
        if not isinstance(name, str):
            print("Product name must be a string.")
            return
        if not (isinstance(price, (int, float)) and price > 0):
            print("Product price must be a positive number.")
            return
        try:
            with self.conn:  
                self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            print(f"Product '{name}' added successfully.")
        except sqlite3.Error as e:
            print("Error adding product:", e)

    def update_product(self, product_id, new_price):
        if not (isinstance(new_price, (int, float)) and new_price > 0):
            print("New price must be a positive number.")
            return
        try:
            with self.conn:
                self.cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
            if self.cursor.rowcount == 0:
                print(f"No product found with id {product_id}.")
            else:
                print(f"Product with id {product_id} updated to new price {new_price}.")
        except sqlite3.Error as e:
            print("Error updating product:", e)

    def delete_product(self, product_id):
        try:
            with self.conn:
                self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            if self.cursor.rowcount == 0:
                print(f"No product found with id {product_id}.")
            else:
                print(f"Product with id {product_id} deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting product:", e)

    def list_products(self):
        try:
            self.cursor.execute("SELECT * FROM products")
            products = self.cursor.fetchall()
            if products:
                for product in products:
                    print(product)
            else:
                print("No products found.")
        except sqlite3.Error as e:
            print("Error listing products:", e)

    def search_products(self, name):
        try:
            search_pattern = f"%{name}%"
            self.cursor.execute("SELECT * FROM products WHERE name LIKE ?", (search_pattern,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error searching products:", e)
            return []

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    p = Product()
    p.add_product("a1", 50)
    print("Listing all products:")
    p.list_products()
    p.update_product(1, 100)
    print("Search results for 'a1':")
    for prod in p.search_products("a1"):
        print(prod)
    p.delete_product(1)
    print("Products after deletion:")
    p.list_products()
