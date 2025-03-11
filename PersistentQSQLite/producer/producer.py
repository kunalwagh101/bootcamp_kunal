import os
import time
import signal
import tempfile
import random
import string
import typer
from persistent.persistentQSQLAlchemy  import PersistentQSQLAlchemy as PersistentQ

app = typer.Typer()
QUEUE = PersistentQ()


interval = int(os.getenv("INTERVAL_TIME", "3"))

def reload_interval(signum, frame):
    """
    Signal handler to reload the producer interval from the environment variable.
    """
    global interval
    try:
        new_interval = int(os.getenv("INTERVAL_TIME", "3"))
        interval = new_interval
        typer.echo(f"Reloaded interval: {interval} seconds.")
    except ValueError:
        typer.echo("Invalid value for INTERVAL_TIME; keeping current interval.")

signal.signal(signal.SIGHUP, reload_interval)

def generate_random_file():
    """
    Generate a unique temporary file with random content.
   
    """
    fd, path = tempfile.mkstemp(prefix="job_", suffix=".txt", text=True)
    with os.fdopen(fd, 'w') as f:
        random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        f.write(f"This is a sample job file with random content: {random_text}\n")
    return os.path.abspath(path)

def submit_job():
    """
    Generate a job file and enqueue it into the persistent queue.
    """
    file_path = generate_random_file()
    typer.echo(f"Produced job: {file_path}")
    QUEUE.enqueue(job_id=file_path, job_data=file_path)

@app.command("run-producer")
def run_producer_cli(cli_interval: int = typer.Option(None,"--interval")):
    """
    Run the job producer that creates new jobs at a specified time interval.
    """
    global interval
    if cli_interval is not None:
        interval = cli_interval
        os.environ["INTERVAL_TIME"] = str(cli_interval)
    typer.echo(f"Starting producer with an interval of {interval} seconds.")
    while True:
        submit_job()
        time.sleep(interval)

if __name__ == "__main__":
    app()
