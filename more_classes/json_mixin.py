

import json

class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls.__new__(cls)  
        obj.__dict__.update(data)
        return obj

class Person(JsonMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

if __name__ == '__main__':
    p = Person("Charlie", 28)
    json_str = p.to_json()
    print("JSON:", json_str)
    p2 = Person.from_json(json_str)
    print("Deserialized:", p2)
