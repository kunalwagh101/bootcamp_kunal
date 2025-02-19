"""
Integrating Exception Handling: Enhance the pipeline with exception handling to
manage potential errors during file reading or processing.
"""


def safe_file_processing_pipeline(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if len(line.strip()) > 0:  
                    try:
                       
                        yield len(line.split())
                    except Exception as e:
                        print(f"Error processing line: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")


if __name__ == '__main__':
    processed_data = list(safe_file_processing_pipeline('sample.txt'))
    print(processed_data)
