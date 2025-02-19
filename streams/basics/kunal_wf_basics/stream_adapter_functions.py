
from typing import Callable, Iterator


StringFunction = Callable[[str], str]
StreamFunction = Callable[[Iterator[str]], Iterator[str]]

def string_to_stream_function(in_function: StringFunction) -> StreamFunction:
  
    def adapted(lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            yield in_function(line)
    return adapted


def capitalize(line: str) -> str:  
    return line.capitalize()


stream_capitalize = string_to_stream_function(capitalize)