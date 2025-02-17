# streamable.py

from abc import ABC, abstractmethod

class Streamable(ABC):
    @abstractmethod
    def stream(self):
        pass

class VideoStream(Streamable):
    def stream(self):
        return "Streaming video..."

class AudioStream(Streamable):
    def stream(self):
        return "Streaming audio..."

if __name__ == '__main__':
    streams = [VideoStream(), AudioStream()]
    for s in streams:
        print(s.stream())

