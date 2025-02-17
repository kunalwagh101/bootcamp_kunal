

def add_hello(cls):
    def say_hello(self):
        return "Hello!"
    cls.say_hello = say_hello
    return cls

@add_hello
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person({self.name})"

if __name__ == '__main__':
    p = Person("Bob")
    print(p)
    print(p.say_hello())
