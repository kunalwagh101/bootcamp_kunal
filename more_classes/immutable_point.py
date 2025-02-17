

class Point:
    def __init__(self, x, y):
        super().__setattr__('x', x)
        super().__setattr__('y', y)
        super().__setattr__('_initialized', True)

    def __setattr__(self, name, value):
        if getattr(self, '_initialized', False):
            raise AttributeError("Point is immutable")
        super().__setattr__(name, value)

    def __str__(self):
        return f"Point({self.x}, {self.y})"

if __name__ == '__main__':
    p = Point(1, 2)
    print(p)
    try:
        p.x = 10  
    except AttributeError as e:
        print("Error:", e)
