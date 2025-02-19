"""
NO.19 functools.total_ordering for Classes: Use total_ordering to simplify class comparison.
Create a class representing a simple 2D point (with x and y coordinates) 
and use functools.total_ordering to compare points based on their distance from the origin.
"""


from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x ** 2 + self.y ** 2) == (other.x ** 2 + other.y ** 2)

    def __lt__(self, other):
        return (self.x ** 2 + self.y ** 2) < (other.x ** 2 + other.y ** 2)
if __name__ == "__main__" :
            p1 = Point(1, 2)
            p2 = Point(2, 2)
            print(p1 < p2)
