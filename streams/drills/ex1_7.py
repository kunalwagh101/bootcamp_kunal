"""
Chaining Iterators: Utilize itertools.chain to combine multiple iterators into one.
Create a combined iterator from several range objects and process them.
"""


import itertools


def process_stream(iterator):
    for item in iterator:
        yield item * 2


combined_iterator = itertools.chain(range(1, 4), range(5, 8), range(10, 13))

if __name__ == '__main__':
    processed = list(process_stream(combined_iterator))
    print(processed) 


