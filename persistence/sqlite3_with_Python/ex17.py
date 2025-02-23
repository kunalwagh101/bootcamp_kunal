"""

NO.17
Updating Multiple Tables in a Transaction: Perform updates across
multiple tables within a transaction.
Create a scenario where you have two related tables
(e.g., orders and order_details). Implement a transaction 
that updates records in both tables, ensuring data consistency across them. Rollback the transaction if any part of the update fails.
"""

import sqlite3

class OrderManager:
    def __init__(self, db_name='store.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cust TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                prod TEXT NOT NULL,
                qty INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')
        self.conn.commit()

    def add_order(self, cust, total, status):
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO orders (cust, total, status) VALUES (?, ?, ?)",
                    (cust, total, status)
                )
            oid = self.cursor.lastrowid
            print(f"Order added (ID: {oid})")
            return oid
        except sqlite3.Error as e:
            print("Add order error:", e)
            return None

    def add_detail(self, order_id, prod, qty, price):
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO details (order_id, prod, qty, price) VALUES (?, ?, ?, ?)",
                    (order_id, prod, qty, price)
                )
            did = self.cursor.lastrowid
            print(f"Detail added (ID: {did})")
            return did
        except sqlite3.Error as e:
            print("Add detail error:", e)
            return None

    def upd_both(self, oid, new_status, new_total, upd_details):

        try:
            self.cursor.execute("BEGIN")
            self.cursor.execute(
                "UPDATE orders SET status = ?, total = ? WHERE id = ?",
                (new_status, new_total, oid)
            )
            if self.cursor.rowcount == 0:
                raise Exception("Order update failed.")
            for did, qty, price in upd_details:
                self.cursor.execute(
                    "UPDATE details SET qty = ?, price = ? WHERE id = ? AND order_id = ?",
                    (qty, price, did, oid)
                )
                if self.cursor.rowcount == 0:
                    raise Exception(f"Detail update failed (ID: {did}).")
            self.conn.commit()
            print("Updates committed.")
        except Exception as e:
            self.conn.rollback()
            print("Update error, rolled back:", e)

    def show_orders(self):
        try:
            self.cursor.execute("SELECT * FROM orders")
            for row in self.cursor.fetchall():
                print(row)
        except sqlite3.Error as e:
            print("Show orders error:", e)

    def show_details(self):
        try:
            self.cursor.execute("SELECT * FROM details")
            for row in self.cursor.fetchall():
                print(row)
        except sqlite3.Error as e:
            print("Show details error:", e)

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    order = OrderManager()
    
  
    oid = order.add_order("A1", 300.0, "Pending")
    if oid:
        val1 = order.add_detail(oid, "Pro A", 2, 50.0)
        val2 = order.add_detail(oid, "Pro B", 3, 50.0)
    
    print("Before update:")
    order.show_orders()
    order.show_details()
    

    if oid and val1 and val2:
        order.upd_both(oid, "Completed", 350.0, [(val1, 3, 55.0), (val2, 2, 60.0)])
    
    print("After update:")
    order.show_orders()
    order.show_details()
