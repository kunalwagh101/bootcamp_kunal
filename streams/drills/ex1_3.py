"""
Using Generators: Convert the custom file reading iterator into a 
generator that yields lines from a file. 
Demonstrate its usage with a sample file
"""


from pathlib import Path

def file_line_generator(filepath):
    """Generator that reads a file line by line, stripping the newline."""
    with open(filepath, 'r') as file:
        for line in file:
            yield line.rstrip('\n')

if __name__ == '__main__':
    file_loc = Path.cwd().joinpath("sample.txt")   
    for line in file_line_generator(file_loc):
        print(line)