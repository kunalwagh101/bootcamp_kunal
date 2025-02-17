"""
NO.14 functools.partial Usage: Learn to use partial from the functools module.
Use functools.partial to create a new function that multiplies any number by 2,
 based on a generic multiplication function.
"""



from functools import partial

def multiply(a, b):
    return a * b
if __name__ == "__main__" :
    double = partial(multiply, 2)
    print(double(5))
