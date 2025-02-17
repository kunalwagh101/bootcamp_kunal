"""
NO.8 Logging Decorator with Parameters: Create a decorator to log with custom messages.
Write a custom_logger decorator that takes a log message and prints 
it before and after the function execution."""



def custom_logger(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@custom_logger("Executing function:")
def example():
    print("Function is running")


if __name__ == "__main__" :
    example()