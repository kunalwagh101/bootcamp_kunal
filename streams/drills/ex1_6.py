"""
File Processing Pipeline: Create a pipeline that reads from a file, filters lines, 
and then processes them (e.g., count the number of words in each line).
"""


def file_processing_pipeline(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if len(line.strip()) > 0:  
                    yield len(line.split())  
    except Exception as e:
        print(f"Error reading file: {e}")


if __name__ == '__main__':

    word_counts = list(file_processing_pipeline('sample.txt'))
    print(word_counts)
