"""
NO.13 Nested List Comprehension: Explore nested list comprehensions.
Use a nested list comprehension to flatten a matrix (a list of lists) into a single list.
"""

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


flattened = [item for row in matrix for item in row]
if __name__ == "__main__" :
        print(flattened)
