
import sys
from pathlib import Path
import time
from prompt_toolkit.shortcuts import button_dialog, input_dialog, message_dialog
from persistent.persistentQSQLAlchemy import PersistentQSQLAlchemy as PersistentQ
import os

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

QUEUE = PersistentQ()

def list_jobs():
    """Display a list of jobs with details."""
    jobs = QUEUE.list_jobs()
    if not jobs:
        message_dialog(title="List Jobs", text="No jobs found.").run()
    else:
        text = "\n".join([f"Job ID: {j[0]}, Status: {j[2]}, Consumer: {j[3]}, Last Consumer: {j[4]}" for j in jobs])
        message_dialog(title="List Jobs", text=text).run()

def assign_job():
    """Prompt for a Job ID and Consumer ID, then assign the job."""
    job_id = input_dialog(title="Assign Job", text="Enter Job ID:").run()
    if not job_id:
        message_dialog(title="Assign Job", text="No Job ID entered.").run()
        return
    consumer_id = input_dialog(title="Assign Job", text="Enter Consumer ID:").run()
    if not consumer_id:
        message_dialog(title="Assign Job", text="No Consumer ID entered.").run()
        return
    if QUEUE.assign_job(job_id, consumer_id):
        message_dialog(title="Assign Job", text=f"Job '{job_id}' assigned to consumer '{consumer_id}' successfully.").run()
    else:
        message_dialog(title="Assign Job", text=f"Failed to assign job '{job_id}'.").run()

def resubmit_job():
    """Prompt for a Job ID, then resubmit the job (set status to pending)."""
    job_id = input_dialog(title="Resubmit Job", text="Enter Job ID:").run()
    if not job_id:
        message_dialog(title="Resubmit Job", text="No Job ID entered.").run()
        return
    if QUEUE.get_job_status(job_id) is None:
        message_dialog(title="Resubmit Job", text="Job not found.").run()
    else:
        QUEUE.update_job_status(job_id, "pending")
        message_dialog(title="Resubmit Job", text=f"Job '{job_id}' resubmitted.").run()

def mark_failed():
    """Prompt for a Job ID, then mark the job as failed."""
    job_id = input_dialog(title="Mark Job Failed", text="Enter Job ID:").run()
    if not job_id:
        message_dialog(title="Mark Job Failed", text="No Job ID entered.").run()
        return
    QUEUE.update_job_status(job_id, "failed")
    message_dialog(title="Mark Job Failed", text=f"Job '{job_id}' marked as failed.").run()

def delete_db_jobs():
    """Delete all job records from the database after confirmation."""
    confirm = button_dialog(
        title="Delete DB Jobs",
        text="Are you sure you want to delete all job records from the database?",
        buttons=[("Yes", True), ("No", False)]
    ).run()
    if confirm:
        if QUEUE.delete_all():
            message_dialog(title="Delete DB Jobs", text="All job records have been deleted.").run()
        else:
            message_dialog(title="Delete DB Jobs", text="Error deleting job records.").run()
    else:
        message_dialog(title="Delete DB Jobs", text="Deletion cancelled.").run()

def delete_job_files():
    """Delete all job files matching 'job_*.txt' in the current directory."""
    from pathlib import Path
    path = Path(".")
    job_files = list(path.glob("job_*.txt"))
    if not job_files:
        message_dialog(title="Delete Job Files", text="No job files found.").run()
        return
    confirm = button_dialog(
        title="Delete Job Files",
        text=f"Found {len(job_files)} job file(s). Delete all?",
        buttons=[("Yes", True), ("No", False)]
    ).run()
    if confirm:
        errors = []
        for job_file in job_files:
            try:
                job_file.unlink()
            except Exception as e:
                errors.append(f"Error deleting {job_file}: {e}")
        if errors:
            message_dialog(title="Delete Job Files", text="\n".join(errors)).run()
        else:
            message_dialog(title="Delete Job Files", text="All job files deleted successfully.").run()
    else:
        message_dialog(title="Delete Job Files", text="Deletion cancelled.").run()

def monitor_jobs():
    """Continuously display the current job list. Press Ctrl+C to stop."""
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            jobs = QUEUE.list_jobs()
            if jobs:
                text = "\n".join([f"Job ID: {j[0]}, Status: {j[2]}, Consumer: {j[3]}, Last Consumer: {j[4] or 'None'}" for j in jobs])
            else:
                text = "No jobs found."
            print("=== Current Jobs ===")
            print(text)
            print("====================")
            time.sleep(5)
    except KeyboardInterrupt:
        message_dialog(title="Monitor", text="Monitoring stopped.").run()

def main():
    """Main loop for the interactive manager TUI."""
    while True:
        choice = button_dialog(
            title="Persistent Queue Manager Interface",
            text="Select an action:",
            buttons=[
                ("List Jobs", "list"),
                ("Assign Job", "assign"),
                ("Resubmit Job", "resubmit"),
                ("Mark Job Failed", "fail"),
                ("Delete DB Jobs", "delete_db"),
                ("Delete Job Files", "delete_files"),
                ("Monitor Jobs", "monitor"),
                ("Exit", "exit")
            ]
        ).run()

        if choice == "list":
            list_jobs()
        elif choice == "assign":
            assign_job()
        elif choice == "resubmit":
            resubmit_job()
        elif choice == "fail":
            mark_failed()
        elif choice == "delete_db":
            delete_db_jobs()
        elif choice == "delete_files":
            delete_job_files()
        elif choice == "monitor":
            monitor_jobs()
        elif choice == "exit":
            break

if __name__ == "__main__":
    main()
