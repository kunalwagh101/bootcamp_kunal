"""
Filtering Data with Iterators: Enhance the file-reading generator
to filter out lines that don't meet a certain condition (e.g., lines not containing a specific word).
"""

from pathlib import Path

class Checkfile():

    def __init__(self,file):
         self.file  = open(file,"r")

    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.file.readline()

        if not line:          
            self.file.close()
            raise StopIteration
        if "!" not in line:  
            return line.rstrip("\n") 
        

def chec_f(keyword,file) :
    with open(file, "r") as lines:
        for line in lines:
            if keyword not in line :
                yield line.strip('\n')
    
if __name__ == '__main__':
    file_loc = Path.cwd().joinpath("sample.txt")   
    value  = chec_f("!", file_loc) 
    for i in value:
        print(i)

    print("======class ======")
    for line in Checkfile(file_loc):
        print(line)