# """
# Basic Class Creation: Create a simple Book class with attributes like title and author.

# Implement the class and create instances of it.
# Static Method Usage: Add a static method to the Book class that validates ISBN numbers.

# Implement and demonstrate its usage without creating an instance of Book.
# Class Method Implementation: Add a class method in the Book class for tracking the number of books created.

# Implement and test this method.
# Using Dunder Methods: Implement the __str__ and __repr__ methods for the Book class.

# Create instances and print them to see the effect of these methods.
# """


class Book :
   
    no_of_books = 0

    def __init__(self, title ,author):
        self.title  = title
        self.author = author
        Book.no_of_books += 1

    def __str__(self):
        return f"title = {self.title} , auther ={self.author} "

    def __str__(self):
        return f"{self.title} by {self.author}"
    

    @classmethod
    def calulate_books(cls):
        return  cls.no_of_books
    

    @staticmethod
    def check_ISBN(code) :

        if len(code) == 10: 
            if not code[:-1].isdigit() or (code[-1] not in "0123456789X"):
                return False
            total = sum((i + 1) * int(d) for i, d in enumerate(code[:-1])) + (10 if code[-1] == 'X' else int(code[-1])) * 10
            return total % 11 == 0
        
        elif len(code) == 13 and code.isdigit():  #
            total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(code))
            return total % 10 == 0

        return False
    


   



if __name__ == "__main__" :
    b1 = Book("autobigraphy of yogi", "xyz")
    value  = True  if b1.check_ISBN("0321543254") else False
    count  = Book.calulate_books()
    print(count)
    print("b1", b1 ,"value = " ,value)

  