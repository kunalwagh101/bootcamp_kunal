import typer
from persistent import get_queue
from pathlib import Path 
import time
import os
import subprocess



QUEUE = get_queue()
app = typer.Typer()

@app.command()
def list_jobs():
    """
    List all jobs with their statuses.
    """
    jobs = QUEUE.list_jobs()
    for job in jobs:
        typer.echo(f"Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]} , consumer_id : {job[3]}")


@app.command()
def failedjobs():
    jobs  = QUEUE.get_all_failed_status()
    if not jobs :
        typer.echo ("Looks like very thing worked for the best, No failed jobs found !")
    for job in  jobs :
        typer.echo(f"Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]} , consumer_id : {job[3]}")
        


@app.command()
def resubmit(job_id: str):
    """
    Resubmit a job by setting its status back to pending.
    """
    if QUEUE.get_job_status(job_id) is None:
        typer.echo("Job not found.")
        raise typer.Exit()
    QUEUE.update_job_status(job_id, "pending")
    typer.echo(f"Job {job_id} resubmitted.")


@app.command()
def delete_job_files(directory: str = "."):
    """
    Delete all local job files .
    """
    path = Path(directory)
    job_files = list(path.glob("job_*.txt"))
    
    if not job_files:
        typer.echo("No job files found.")
        raise typer.Exit()

    typer.echo(f"Found {len(job_files)} job file(s) in '{directory}'.")
    confirm = typer.confirm("Are you sure you want to delete all these job files?")
    if not confirm:
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
    """
    confirm = typer.confirm("Are you sure you want to delete all job records from the database?")
    if not confirm:
        typer.echo("Deletion cancelled.")
        raise typer.Exit()
    
    message = QUEUE.delete_all()
    if not message :
        typer.echo("Error deleting jobs from the database")
    typer.echo("All job records have been deleted from the database.")




@app.command()
def assign_job(job_id: str, consumer_id: str):
    """
    Assign or reassign a job to a specified consumer.

    """
    confirm = typer.confirm(f"Are you sure you want to assign job '{job_id}' to consumer '{consumer_id}'?")
    if not confirm:
        typer.echo("Assignment cancelled.")
        raise typer.Exit()

    success = QUEUE.assign_job(job_id, consumer_id)
    if success:
        typer.echo(f"Job '{job_id}' has been assigned to consumer '{consumer_id}'.")
        try:
            subprocess.Popen(["poetry", "run", "python", "-m", "consumer.consumer"])
            typer.echo("Consumer process started.")
        except Exception as e:
            typer.echo(f"Failed to start consumer process: {e}")
    else:
        typer.echo(f"Failed to assign job '{job_id}'. Please ensure the job exists.")




@app.command()
def monitor(interval: int = 5):
    """
    Monitor job status in real time.
    """
    try:
        while True:
           
            os.system("clear")
            jobs = QUEUE.list_jobs()
            if jobs:
                typer.echo("Current Jobs:")
                for job in jobs:
                    typer.echo(f"consumer_id : {job[3]} ,Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]}")
            else:
                typer.echo("No jobs found.")
            time.sleep(interval)
    except KeyboardInterrupt:
        typer.echo("Monitoring stopped.")

if __name__ == "__main__":
    app()


@app.command()
def mark_failed(job_id: str):
    """
    Mark a job as failed.
    """
    QUEUE.update_job_status(job_id, "failed")
    typer.echo(f"Job {job_id} marked as failed.")

if __name__ == "__main__":
    app()
