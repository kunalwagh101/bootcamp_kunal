"""
NO.16 List Comprehension with Multiple Iterables: Use multiple iterables in a list comprehension.
Generate all possible pairs (as tuples) of numbers from two different lists using a list comprehension
"""




from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
if __name__ == "__main__" :
        print(fibonacci(50))
