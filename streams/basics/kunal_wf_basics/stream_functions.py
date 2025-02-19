
from typing import Iterator



def number_the_lines(lines: Iterator[str]) -> Iterator[str]:
    
    for i, line in enumerate(lines, start=1):
        yield f"{i}: {line}"

def coalesce_empty_lines(lines: Iterator[str]) -> Iterator[str]:
  
    previous_was_empty = False
    for line in lines:
        if line.strip() == "":
            if not previous_was_empty:
                yield line
                previous_was_empty = True
        else:
            previous_was_empty = False
            yield line

def break_lines(lines: Iterator[str], width: int = 20) -> Iterator[str]:
 
    for line in lines:
        line = line.rstrip("\n")
        if len(line) <= width:
            yield line
        else:
            for i in range(0, len(line), width):
                yield line[i:i+width]



def remove_empty_lines(lines: Iterator[str]) -> Iterator[str]:
  
    for line in lines:
        if line.strip() != "":
            yield line

def remove_even_lines(lines: Iterator[str]) -> Iterator[str]:

    for i, line in enumerate(lines, start=1):
        if i % 2 != 0:
            yield line



if __name__ == "__main__":
  
    sample_lines = [
        "This is the first line.",
        "",
        "",
        "This is a very long line that should be broken up into smaller chunks when processed by break_lines.",
        "Another line here.",
        "",
        "Yet another line to test coalesce_empty_lines and remove_empty_lines.",
        "",
        "",
        "Final line."
    ]
    
    print("Original lines:")
    for line in sample_lines:
        print(repr(line))
    
    print("\nNumbered lines:")
    for line in number_the_lines(iter(sample_lines)):
        print(line)
    
    print("\nCoalesce empty lines:")
    for line in coalesce_empty_lines(iter(sample_lines)):
        print(repr(line))
    
    print("\nRemove empty lines:")
    for line in remove_empty_lines(iter(sample_lines)):
        print(repr(line))
    
    print("\nRemove even lines:")
    for line in remove_even_lines(iter(sample_lines)):
        print(repr(line))
    
    print("\nBreak lines (width=20):")
    for line in break_lines(iter(sample_lines), width=20):
        print(repr(line))
