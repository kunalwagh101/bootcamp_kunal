"""
Advanced Stream Processing: Develop a complex stream processing pipeline that reads from multiple files, filters, processes data,
 and writes the results to a new file. Include error handling and efficiency considerations

"""
from pathlib import Path

def file_iterator(filenames):
    """Generator to iterate over multiple files line by line."""
    for filename in filenames:
        file_path = Path(filename)
        try:
            with file_path.open('r', encoding='utf-8') as f:
                for line in f:
                    yield line.strip()
        except (FileNotFoundError, IOError) as e:
            print(f"Error reading {filename}: {e}")

def filter_data(iterator):
    """Filter lines that are non-empty and do not start with # (comment)."""
    return (line for line in iterator if line and not line.startswith('#'))

def process_data(iterator):
    """Process data by converting it to uppercase."""
    return (line.upper() for line in iterator)

def write_output(iterator, output_file):
    """Write processed data to an output file."""
    output_path = Path(output_file)
    try:
        with output_path.open('w', encoding='utf-8') as f:
            for line in iterator:
                f.write(line + '\n')
        print(f"Processed data written to {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    input_files = ['sample.txt', 'sample2.txt']
    output_file = 'output.txt'
    
    lines = file_iterator(input_files)
    filtered_lines = filter_data(lines)
    processed_lines = process_data(filtered_lines)
    write_output(processed_lines, output_file)