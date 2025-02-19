

def numbers(end_value):
    a = 0
    b = 1
    for _ in range(end_value):
        a , b  =  b , a+b 
        yield a 

def fib(end_value=20):
    for i in numbers(end_value):
        print(i)

def skips(end_value=100):

    fib_gen = numbers(end_value)
  
    for _ in range(10):
        next(fib_gen)
  
    for _ in range(10):
        yield next(fib_gen)


def str_range(n: int=10): 
    for i in range(n):
        yield f"line number {i}"



def get_str_range(n: int=20):
    return list(str_range(n))



if __name__ == "__main__":

    print("=== fibonnaci ==== ",'\n')
    fib(30)
    print("=== skip the 10 number ===",'\n')
    for num in skips():
        print(num)

    print("==== line number {i} ====",'\n')

    for i in str_range():
        print(i)

    print("=== iterate over the first 20 strings ===",'\n')
    print(get_str_range())



