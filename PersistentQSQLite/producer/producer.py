import time
import os
import random
import string
from persistent import get_queue

QUEUE = get_queue()

def generate_random_file():
    
    filename = f"job_{int(time.time())}_{''.join(random.choices(string.ascii_lowercase, k=5))}.txt"
    with open(filename, "w") as f:
        f.write("This is a sample job file.\n")
    return os.path.abspath(filename)

def submit_job():
    file_path = generate_random_file()
    print(f"Produced job: {file_path}")
    QUEUE.enqueue(job_id=file_path, job_data=file_path)

def main():
    while True:
        submit_job()
        time.sleep(5)

if __name__ == "__main__":
    main()
