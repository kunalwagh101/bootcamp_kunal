"""
No.14 Exporting Data: Write a function to export data from the products table to a CSV file.
The function should query the database and write the results to a CSV file.
"""

import sqlite3
import csv

class Product:
    def __init__(self, db_name='store.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
      
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        self.conn.commit()

    def add_category(self, name):
        if not isinstance(name, str):
            print("Category name must be a string.")
            return
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            print(f"Category '{name}' added successfully.")
        except sqlite3.Error as e:
            print("Error adding category:", e)

    def add_product(self, name, price, category_id=None):
        if not isinstance(name, str):
            print("Product name must be a string.")
            return
        if not (isinstance(price, (int, float)) and price > 0):
            print("Product price must be a positive number.")
            return
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)",
                    (name, price, category_id)
                )
            print(f"Product '{name}' added successfully.")
        except sqlite3.Error as e:
            print("Error adding product:", e)

    def update_product(self, product_id, new_price):
        if not (isinstance(new_price, (int, float)) and new_price > 0):
            print("New price must be a positive number.")
            return
        try:
            with self.conn:
                self.cursor.execute(
                    "UPDATE products SET price = ? WHERE id = ?",
                    (new_price, product_id)
                )
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

    def fetch_prod_categories(self):
      
        try:
            self.cursor.execute('''
                SELECT p.id, p.name, p.price, c.name AS category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error fetching products with categories:", e)
            return []

    def export_prod_to_csv(self, filename):
       
        try:
   
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["id", "name", "price", "category_id"])
            
                self.cursor.execute("SELECT id, name, price, category_id FROM products")
                rows = self.cursor.fetchall()            
                writer.writerows(rows)
            print(f"Data exported successfully to {filename}")
        except Exception as e:
            print("Error exporting data:", e)

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    p = Product()
    p.add_category("car")
    p.add_product("bike", 1000, 1)
    p.add_product("plane", 25)  


    print("Listing all products:")
    p.list_products()

    print("\nProducts with categories:")
    for prod in p.fetch_prod_categories():
        print(prod)
    
    
    p.export_prod_to_csv("products_export.csv")
