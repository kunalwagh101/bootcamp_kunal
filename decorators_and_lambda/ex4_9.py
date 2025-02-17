"""
NO.9 Class Method Decorator: Apply a decorator to class methods.
Implement a validate_args decorator that checks and validates 
the arguments passed to any class method in which it is used.
"""


def validate_args(func):
    def wrapper(self, *args):
        if any(a < 0 for a in args):
            raise ValueError("Negative values not allowed")
        return func(self, *args)
    return wrapper

class Calculator:
    @validate_args
    def add(self, a, b):
        return a + b
    

if __name__ == "__main__" :
    calc = Calculator()
    print(calc.add(3, 4))

