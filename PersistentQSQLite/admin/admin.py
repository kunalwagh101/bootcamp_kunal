import os
import time
import typer
from pathlib import Path
from persistent.persistentQSQLAlchemy import PersistentQSQLAlchemy as PersistentQ

QUEUE = PersistentQ()
app = typer.Typer()

@app.command()
def list_jobs():
    """
    List all jobs with details: job_id, job_data, status, and consumer_id.
    """
    jobs = QUEUE.list_jobs()
    for job in jobs:
        typer.echo(f"Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]}, Consumer: {job[3]}")

@app.command()
def resubmit(job_id: str):
    """
    Resubmit a job by setting its status back to 'pending'.
    """
    if QUEUE.get_job_status(job_id) is None:
        typer.echo("Job not found.")
        raise typer.Exit()
    QUEUE.update_job_status(job_id, "pending")
    typer.echo(f"Job {job_id} resubmitted.")

@app.command()
def mark_failed(job_id: str):
    """
    Mark a job as 'failed'.
    """
    QUEUE.update_job_status(job_id, "failed")
    typer.echo(f"Job {job_id} marked as failed.")

@app.command()
def delete_job_files(directory: str = "."):
    """
    Delete all job files (matching 'job_*.txt') in the specified directory.
    Asks for confirmation before deletion.
    """
    path = Path(directory)
    job_files = list(path.glob("job_*.txt"))
    if not job_files:
        typer.echo("No job files found.")
        raise typer.Exit()
    typer.echo(f"Found {len(job_files)} job file(s) in '{directory}'.")
    if not typer.confirm("Are you sure you want to delete all these job files?"):
        typer.echo("Deletion cancelled.")
        raise typer.Exit()
    for job_file in job_files:
        try:
            job_file.unlink()
            typer.echo(f"Deleted: {job_file}")
        except Exception as e:
            typer.echo(f"Error deleting {job_file}: {e}")
    typer.echo("All job files deleted.")

@app.command()
def delete_db_jobs():
    """
    Delete all job records from the persistent queue database.
    Asks for confirmation before deletion.
    """
    if not typer.confirm("Are you sure you want to delete all job records from the database?"):
        typer.echo("Deletion cancelled.")
        raise typer.Exit()
    if QUEUE.delete_all():
        typer.echo("All job records have been deleted from the database.")
    else:
        typer.echo("Error deleting jobs from the database.")

@app.command()
def assign_job(job_id: str, consumer_id: str):
    """
    Assign (or reassign) a job to a specified consumer.
    Updates the job's consumer_id and marks it as 'processing'.
    """
    if not typer.confirm(f"Are you sure you want to assign job '{job_id}' to consumer '{consumer_id}'?"):
        typer.echo("Assignment cancelled.")
        raise typer.Exit()
    if QUEUE.assign_job(job_id, consumer_id):
        typer.echo(f"Job '{job_id}' has been assigned to consumer '{consumer_id}'.")
    else:
        typer.echo(f"Failed to assign job '{job_id}'. Please ensure the job exists.")

@app.command()
def monitor(interval: int = 5):
    """
    Monitor job statuses in real time.
    Clears the screen and displays current job details every 'interval' seconds.
    Press Ctrl+C to exit.
    """
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            jobs = QUEUE.list_jobs()
            if jobs:
                typer.echo("Current Jobs:")
                for job in jobs:
                    typer.echo(f"Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]}, Consumer: {job[3]}")
            else:
                typer.echo("No jobs found.")
            time.sleep(interval)
    except KeyboardInterrupt:
        typer.echo("Monitoring stopped.")

if __name__ == "__main__":
    app()
