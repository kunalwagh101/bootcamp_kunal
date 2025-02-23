"""
No.13
Aggregation Queries: Add a method to calculate the total value of all products in stock.
This method should sum the price of all products and return the total.
"""


import sqlite3
from ex12 import Product


class Aggregator(Product):
    def total_value(self):
    
        try:
            self.cursor.execute("SELECT SUM(price) FROM products")
            result = self.cursor.fetchone()[0]
        
            return result if result is not None else 0
        except sqlite3.Error as e:
            print("Error calculating total value:", e)
            return None

if __name__ == '__main__':
    aggregator = Aggregator()
   
    aggregator.add_product("a1", 50)
    aggregator.add_product("a2", 75)
    aggregator.add_product("a3", 125)

    print("Listing all products:")
    aggregator.list_products()

    total = aggregator.total_value()
    print(f"\nTotal value of all products: {total}")