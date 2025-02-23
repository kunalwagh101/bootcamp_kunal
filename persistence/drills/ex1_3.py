"""
No.3  JSON Serialization: Convert a Book object to a JSON string.
Implement a method in the Book class to return its JSON representation.
"""

import json

class Book:
    def __init__(self, title, author, pages, published_year):
        self.title = title
        self.author = author
        self.pages = pages
        self.published_year = published_year

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, pages={self.pages}, published_year={self.published_year})"

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

if __name__ == "__main__":
    book = Book(title="1984", author="George Orwell", pages=328, published_year=1949)
    
  
    book_json = book.to_json()
    print("Serialized JSON:\n", book_json)

   
    new_book = Book.from_json(book_json)
    print("\nDeserialized Object:\n", new_book)
