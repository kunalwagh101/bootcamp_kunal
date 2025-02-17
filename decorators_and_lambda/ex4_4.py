""" NO.4 Memoization Decorator: Create a decorator for caching function results.
Write a memoize decorator that caches the return values of a function, so repeated calls with the same arguments return the cached result.
"""



def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__" :
     fibonacci(3)


