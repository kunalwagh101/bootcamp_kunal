

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        # If other is a number, perform scalar multiplication
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        # If other is a Vector, return the dot product
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

if __name__ == '__main__':
    v1 = Vector(2, 3)
    v2 = Vector(4, 1)
    print("v1 + v2 =", v1 + v2)
    print("v1 - v2 =", v1 - v2)
    print("v1 * 3 =", v1 * 3)
    print("Dot product of v1 and v2 =", v1 * v2)
    print("3 * v2 =", 3 * v2)
