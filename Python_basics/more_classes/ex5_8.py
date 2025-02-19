""""
No.8 Abstract Properties: Add abstract properties to an abstract bas
 class and implement them in child classes.
Example: abstract class Animal with an abstract property sound.

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
