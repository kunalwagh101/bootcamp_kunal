"""
NO.12 Conditional List Comprehension: Use a condition within a list comprehension.
Create a list of even numbers from 1 to 20 using a list comprehension with a conditional statement.
"""


even_numbers = [x for x in range(1, 21) if x % 2 == 0]
if __name__ == "__main__" :
    print(even_numbers)
