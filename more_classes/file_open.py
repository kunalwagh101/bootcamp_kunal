

class FileOpen:
    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

if __name__ == '__main__':

    with FileOpen("test.txt", "w") as f:
        f.write("Hello, world!")

   
    with FileOpen("test.txt", "r") as f:
        content = f.read()
        print("File content:", content)
