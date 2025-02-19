"""NO.5 Debug Information Decorator: Build a decorator to print function details.
Implement a debug_info decorator that prints the name of the function, 
its arguments, and its return value each time the function is called."""




def debug_info(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@debug_info
def add(a, b):
    return a + b



if __name__ == "__main__" :
    add(3, 5)


