"""
NO.11 Simple List Comprehension: Practice creating a list comprehension.
Generate a list of squares for numbers from 1 to 10 using a list comprehension.
"""

squares = [x ** 2 for x in range(1, 11)]
evens = [x for x in range(1, 21) if x % 2 == 0]
matrix = [[1, 2], [3, 4]]
flattened = [num for row in matrix for num in row]

if __name__ == "__main__" :

    print(squares)
    print(evens)
    print(flattened)
