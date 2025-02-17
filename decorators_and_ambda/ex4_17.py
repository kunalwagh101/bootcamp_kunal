"""
NO.17 functools.lru_cache for Optimization: Optimize a recursive function with lru_cache.
Write a recursive function to calculate Fibonacci numbers and use functools.lru_cache to optimize it.
"""



from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)



if __name__ == "__main__" :
    print(fibonacci(50))