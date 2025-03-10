import time
import tempfile
import os
import random
import string
from persistent.persistentQSQLAlchemy import PersistentQSQLAlchemy as PersistentQ

QUEUE = PersistentQ()

def generate_random_file():
    """
    Generate a unique temporary file with random content.
    Returns the absolute file path.
    """
    fd, path = tempfile.mkstemp(prefix="job_", suffix=".txt", text=True)
    with os.fdopen(fd, 'w') as f:
        random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        f.write(f"This is a sample job file with random content: {random_text}\n")
    return os.path.abspath(path)

def submit_job():
    """
    Generate a job file and enqueue it.
    """
    file_path = generate_random_file()
    print(f"Produced job: {file_path}")
    QUEUE.enqueue(job_id=file_path, job_data=file_path)

def main():
    """
    Continuously produce jobs every 5 seconds.
    """
    while True:
        submit_job()
        time.sleep(5)

if __name__ == "__main__":
    main()
