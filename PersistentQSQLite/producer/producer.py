import time
import tempfile
import os
import random
import string
from persistent.persistentQSQLAlchemy import PersistentQSQLAlchemy as PersistentQ
import typer
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


app = typer.Typer()


@app.command()
def run_producer(interval: int = 5):
    """
    Run the job producer that creates new jobs at a specified time interval (in seconds).
    """
    typer.echo(f"Starting producer with an interval of {interval} seconds.")
    while True:
        submit_job()
        time.sleep(interval)

if __name__ == "__main__":
    app()
