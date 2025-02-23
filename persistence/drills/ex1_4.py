
"""
JSON Deserialization: Create a Book object from a JSON string.
Write a class method to create a Book instance from its JSON string representation.
"""


from ex1_3  import Book
import json

class Convertor(Book):
    def __init__(self, title, author, pages, published_year):
        super().__init__(title, author, pages, published_year)

        self.obj =  Book(self.title, self.author, self.pages, self.published_year)

    def convertor_json(self):
        return self.obj.to_json()
    
    @classmethod
    def json_to(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)
   


if __name__ == "__main__" :

    obj1 = Convertor("top","andrew car" , "254" ,"2008")
    jfile = obj1.convertor_json()
    print("Book object converted to the json =" ,jfile )
    print("json converted to the object" , Convertor.json_to(jfile))
    

