""" 
Decorator with Arguments: Create a decorator that can take arguments.

Write a decorator named prefix_printer that takes a string prefix
and prints it before the function's name each time the function is called.
"""

def prefix_printer(prefix) :
    def deco(fun) :
        def wrapper(*args, **kwargs) :        
            print(prefix)
            main = fun(*args, **kwargs)

            return main   
        return wrapper
    return deco




@prefix_printer("this is prefix")
def example():
    print("hello")


if __name__ == "__main__" :
    example()

