"""
NO.10 Composition of Decorators: Practice combining multiple decorators.
Combine simple_logger, timer, and debug_info decorators 
in different orders on a single function and observe the output differences.
"""

from ex4_3 import measure
from ex4_5 import debug_info
from ex4_8 import custom_logger
@measure
@debug_info
@custom_logger
def complex_function(x):
    return x ** 2


if __name__ == "__main__" :
    complex_function(5)
