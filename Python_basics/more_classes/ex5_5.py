"""
NO 5. Implementing an Abstract Base Class (ABC): Create an abstract base class
Shape with an abstract method area.
Derive subclasses like Circle and Rectangle, implementing area in each.
"""

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def __str__(self):
        return f"Circle(radius={self.radius})"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

if __name__ == '__main__':
    shapes = [Circle(5), Rectangle(4, 6)]
    for shape in shapes:
        print(f"{shape} has area: {shape.area()}")
