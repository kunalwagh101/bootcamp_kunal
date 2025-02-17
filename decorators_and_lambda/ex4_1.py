"""
No.1 Basic Function Decorator: Learn to write a basic decorator for a function.
Create a decorator named simple_logger that prints 
"Function started" and "Function ended" when any function is called.
"""



def simple_logger(fun):
    def wrapper(*args ,**kwargs) :
        print("Function started")
        final = fun(*args, **kwargs)
        print("Function ended")
        return final
    return wrapper

@simple_logger
def example():
    print("hello")


if __name__ == "__main__" :
    example()