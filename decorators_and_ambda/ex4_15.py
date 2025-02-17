"""
NO.15 Combining functools.reduce with Lambda: Implement reduce with a lambda function.
Utilize functools.reduce and a lambda function to calculate the factorial of a number.
"""


from functools import reduce

factorial = lambda n: reduce(lambda x, y: x * y, range(1, n + 1), 1)


if __name__ == "__main__" :
        print(factorial(5))