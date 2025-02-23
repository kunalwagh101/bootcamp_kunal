"""
No 19
Transactional Banking Operations: Simulate a banking transaction.
Create a scenario involving transferring funds from one account to another (e.g., accounts table with account_id and balance columns). Ensure that the debit from one account and the credit to another are done in a
 single transaction, rolling back if either operation fails.
"""


import sqlite3

def database():
    # Assign the connection to 'conn'
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY,
            balance REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def transfer_funds(source_account_id, dest_account_id, amount):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (source_account_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Source account not found.")
        
        source_balance = row[0]
        if source_balance < amount:
            raise Exception("Insufficient funds in the source account.")
        
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
            (amount, source_account_id)
        )
        
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
            (amount, dest_account_id)
        )
        
        conn.commit()
        print(f"Transaction successful: Transferred ${amount:.2f} from account {source_account_id} to account {dest_account_id}.")
    
    except Exception as e:
        conn.rollback()
        print("Transaction failed and rolled back:", e)
    
    finally:
        conn.close()

if __name__ == "__main__":
    database()
    
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO accounts (account_id, balance) VALUES (1, 1000.0)")
    cursor.execute("INSERT OR IGNORE INTO accounts (account_id, balance) VALUES (2, 500.0)")
    conn.commit()
    conn.close()
    
    transfer_funds(50, 100, 200.0)
