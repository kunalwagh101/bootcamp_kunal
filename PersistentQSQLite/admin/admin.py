import typer
from persistent.persistent import PersistentQSQLite

QUEUE = PersistentQSQLite()
app = typer.Typer()

@app.command()
def list_jobs():
    """
    List all jobs and their statuses.
    """
    jobs = QUEUE.list_jobs()
    for job in jobs:
        typer.echo(f"Job ID: {job[0]}, Data: {job[1]}, Status: {job[2]}")

@app.command()
def resubmit(job_id: str):
    """
    Resubmit a job by setting its status to pending.
    """
    if QUEUE.get_job_status(job_id) is None:
        typer.echo("Job not found.")
        raise typer.Exit()
    QUEUE.update_job_status(job_id, "pending")
    typer.echo(f"Job {job_id} resubmitted.")

@app.command()
def mark_failed(job_id: str):
    """Mark a job as unprocessable (failed)."""
    QUEUE.update_job_status(job_id, "failed")
    typer.echo(f"Job {job_id} marked as failed.")

if __name__ == "__main__":
    app()
