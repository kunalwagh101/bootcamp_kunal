"""
Handling Large Files Efficiently: Modify the file processing pipeline 
to handle large files efficiently without loading the entire file into memory.
"""

def large_file_processing_pipeline(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield len(line.split())
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    word_counts_large = list(large_file_processing_pipeline('sample.txt'))
    print(word_counts_large)
