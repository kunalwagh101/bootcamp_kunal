""""
No5.Implementing an Abstract Base Class (ABC): Create an abstract base
class Shape with an abstract method area.
Derive subclasses like Circle and Rectangle, implementing area in each.
"""


from abc import ABC, abstractmethod

class Animal(ABC):
    @property
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    @property
    def sound(self):
        return "Woof!"

class Cat(Animal):
    @property
    def sound(self):
        return "Meow!"

if __name__ == '__main__':
    animals = [Dog(), Cat()]
    for animal in animals:
        print(f"{animal.__class__.__name__} says: {animal.sound}")
