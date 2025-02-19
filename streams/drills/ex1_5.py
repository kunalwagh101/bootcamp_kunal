"""
Creating a Stream Processing Function: Write a function that takes
an iterator as input and processes its items,
e.g., multiplying numbers by 2. Test this with a range iterator.
"""




def process_stream(iterator):
    for item in iterator:
        yield item * 2

if __name__ == '__main__':
    range_iterator = iter(range(1, 6))
    processed = list(process_stream(range_iterator))
    print(processed)  
