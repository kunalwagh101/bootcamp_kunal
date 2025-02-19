"""
No.Custom Iterator for File Reading: Write a custom iterator that reads a file line by line.
 Test this by reading a sample text file and printing each line.
"""
from pathlib import Path
class CheckLine() :

    def __init__(self,file):
        self.file  =  open(file,"r")

    def __iter__(self):
        return self
    
    def __next__(self):
        line  = self.file.readline()
        
        if line :
            return line.rstrip()
        
        self.file.close()
        raise StopIteration
    
if __name__ == "__main__":
     
    file_loc = Path.cwd().joinpath("sample.txt")      
    file_iterator = CheckLine(file_loc)

    for line in file_iterator:
        print(line)