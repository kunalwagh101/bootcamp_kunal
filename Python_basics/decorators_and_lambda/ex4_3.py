"""
NO.3 Timing Decorator: Implement a decorator to measure execution time.
Develop a timer decorator that prints the time taken by a function to execute.
"""


import time

def measure(fun):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter() 
        result = fun(*args, **kwargs)    
        end_time = time.perf_counter()   
        elapsed_time = end_time - start_time
        print(f"Execution time of {fun.__name__}: {elapsed_time:.6f} seconds")
        return result  
    return wrapper


@measure
def example():
    print("this is example")


if __name__ == "__main__" :
    example()

