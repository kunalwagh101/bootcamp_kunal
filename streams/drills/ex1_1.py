"""
No.1 Basic Iterator Creation: Create a simple iterator that yields numbers from 1 to 10. 
Use a for loop to iterate over this iterator and print the numbers.
"""


def iterator_fun():  
    for num in range(0,10) :
        yield num

def example():
    value = iterator_fun()
    for i in range(0,11):
        nxt_val = next(value,None)
        if nxt_val:
            print(f"{i} * {nxt_val} == {i*nxt_val}")



if __name__ == "__main__":
 
    print(example())
    
