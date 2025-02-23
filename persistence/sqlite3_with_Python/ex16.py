"""
No.16
Basic Transaction Handling: Implement a basic transaction.
Write a script to start a transaction, insert multiple records into a table (e.g., customers), and commit the transaction. Include error handling to rollback the transaction in case of any failures.

"""


import sqlite3

class CustomerManager:
    def __init__(self, db_name='store.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
      
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    def insert_customers(self, customers):

        try:
            self.cursor.execute("BEGIN")     
            self.cursor.executemany(
                "INSERT INTO customers (name, email) VALUES (?, ?)",
                customers
            )
           
            self.conn.commit()
            print("Customers inserted successfully. Transaction committed.")
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Error inserting customers, transaction rolled back:", e)

    def list_customers(self):
        """List all customers from the customers table."""
        try:
            self.cursor.execute("SELECT * FROM customers")
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No customers found.")
        except sqlite3.Error as e:
            print("Error listing customers:", e)

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    manager = CustomerManager()
    
 
    customers_to_insert = [
        ("A", "a@example.com"),
        ("B", "b@example.com"),
        ("C", "c@example.com")
    ]
    
  
    manager.insert_customers(customers_to_insert)
    print("\nListing all customers:")
    manager.list_customers()
