"""
NO.18 Advanced List Comprehension: Implement more complex logic in a list comprehension.
Create a list comprehension that transforms all strings in a list to uppercase and all integers to their square values.
"""


data = ['hello', 3, 'world', 7, 'python', 10]
transformed = [x.upper() if isinstance(x, str) else x**2 for x in data]


if __name__ == "__main__" :
    print(transformed)  
