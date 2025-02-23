"""
No.18
Batch Inserts with Transaction: Use a transaction for batch data insertion.
Write a function that accepts a list of data records (e.g., product information) and inserts them into a table using a single transaction.
 The transaction should rollback if any record fails to insert.
"""


import sqlite3

def batch_insert_products(records):
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()

    try:

        cursor.execute('BEGIN')
        for record in records:
            cursor.execute(
                'INSERT INTO products (id, name, price) VALUES (?, ?, ?)',
                (record['id'], record['name'], record['price'])
            )
        
        conn.commit()
        print("All records inserted successfully.")
    
    except Exception as e:
        conn.rollback()
        print("Transaction rolled back due to error:", e)
    
    finally:
        conn.close()


if __name__ == "__main__":
    product_data = [
        {'id': 1, 'name': 'Product A', 'price': 19.99},
        {'id': 2, 'name': 'Product B', 'price': 29.99},
        {'id': 3, 'name': 'Product C', 'price': 39.99}
    ]
    batch_insert_products(product_data)
