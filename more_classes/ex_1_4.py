


"""
NO.1 Basic Class Creation: Create a simple Book class with attributes like title and author.

NO.2 Implement the class and create instances of it.
Static Method Usage: Add a static method to the Book class that validates ISBN numbers.

NO.3 Implement and demonstrate its usage without creating an instance of Book.
Class Method Implementation: Add a class method in the Book class for tracking the number of books created.
Implement and test this method.

NO.4 Using Dunder Methods: Implement the __str__ and __repr__ methods for the Book class.
Create instances and print them to see the effect of these methods.
"""

class Book:
    book_count = 0  

    def __init__(self, title, author, isbn=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        Book.book_count += 1

    @staticmethod
    def validate_isbn(isbn):
        """
        Validates an ISBN.
    
        """
        if len(isbn) == 10:
            return isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X')
        elif len(isbn) == 13:
            return isbn.isdigit()
        else:
            return False

    @classmethod
    def get_book_count(cls):
        """Returns the total number of Book instances created."""
        return cls.book_count

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"



if __name__ == '__main__':
    book1 = Book("1984", "hwfaip", isbn="123456789X")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", isbn="9780060935467")
    
    print(book1)              
    print(repr(book2))      

    print("ISBN 123456789X valid?", Book.validate_isbn("123456789X"))
    print("ISBN 9780060935467 valid?", Book.validate_isbn("9780060935467"))
    print("Total books created:", Book.get_book_count())
