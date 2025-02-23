"""
No 20
Complex Business Logic with Transactions: Implement a transaction involving complex business logic.
Develop a script to handle inventory management (e.g., products and inventory_log tables). The transaction should update the inventory count of a product and log the change in the inventory_log table. 
Ensure the entire operation is 
atomic and consistent, using transaction rollback for error handling.
"""

from ex15 import Product
import sqlite3


class InventoryManager(Product):
    def __init__(self, db_name='store.db'):
        super().__init__(db_name)

        try:
            self.cursor.execute("ALTER TABLE products ADD COLUMN inventory INTEGER DEFAULT 0")
            self.conn.commit()
        except sqlite3.Error:
            pass
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                change INTEGER NOT NULL,
                reason TEXT,
                log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        self.conn.commit()

    def update_inventory(self, product_id, delta, reason):
    
        try:
            self.cursor.execute("BEGIN")
            self.cursor.execute(
                "UPDATE products SET inventory = inventory + ? WHERE id = ?",
                (delta, product_id)
            )
            if self.cursor.rowcount == 0:
                raise Exception("Product not found or inventory update failed.")
            self.cursor.execute(
                "INSERT INTO inventory_log (product_id, change, reason) VALUES (?, ?, ?)",
                (product_id, delta, reason)
            )
            self.conn.commit()
            print("Inventory updated and logged successfully.")
        except Exception as e:
            self.conn.rollback()
            print("Error updating inventory, transaction rolled back:", e)

    def list_inventory(self):
        try:
            self.cursor.execute("SELECT id, name, inventory FROM products")
            for row in self.cursor.fetchall():
                print(row)
        except sqlite3.Error as e:
            print("Error listing inventory:", e)

    def list_inv_log(self):
        try:
            self.cursor.execute("SELECT * FROM inventory_log")
            for row in self.cursor.fetchall():
                print(row)
        except sqlite3.Error as e:
            print("Error listing inventory log:", e)

if __name__ == '__main__':
    inv_mgr = InventoryManager()

   
    inv_mgr.add_category("car")
    inv_mgr.add_product("bike", 1000, 1)
    inv_mgr.add_product("plane", 25)  

    print("Products before inventory update:")
    inv_mgr.list_products()
    inv_mgr.update_inventory(1, 10, "Restock")
    print("\nInventory after update:")
    inv_mgr.list_inventory()

    print("\nInventory log:")
    inv_mgr.list_inv_log()