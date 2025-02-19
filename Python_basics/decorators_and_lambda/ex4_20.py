"""
NO.20 Combining functools with List Comprehensions: Integrate functools with list comprehensions.
Use functools.reduce along with a list comprehension to calculate the sum of squares of numbers from 1 to 10.
"""


from functools import reduce

sum_of_squares = reduce(lambda x, y: x + y, [x**2 for x in range(1, 11)])

if __name__ == "__main__" :
    print(sum_of_squares) 
