

def init(self, name, age):
    self.name = name
    self.age = age

def greet(self):
    return f"Hello, my name is {self.name} and I am {self.age} years old."

DynamicPerson = type('DynamicPerson', (object,), {
    '__init__': init,
    'greet': greet,
    '__str__': lambda self: f"DynamicPerson(name={self.name}, age={self.age})"
})

if __name__ == '__main__':
    person = DynamicPerson("Alice", 30)
    print(person)
    print(person.greet())
