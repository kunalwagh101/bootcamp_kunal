import time
import random
from datetime import datetime
from persistent.persistent import PersistentQSQLite

QUEUE = PersistentQSQLite()

def process_job(job_id: str, job_data: str):
    """
    processes a job by reading a file, 
    """
    try:
        with open(job_data, "r") as f:
            lines = f.readlines()
    
        timestamp = datetime.now().isoformat()
        processed_lines = [f"{timestamp} {line}" for line in lines]
        with open(job_data, "w") as f:
            f.writelines(processed_lines)
        print(f"Processed job: {job_id}")
        QUEUE.update_job_status(job_id, "completed")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        QUEUE.update_job_status(job_id, "failed")

def main():
    while True:
        job = QUEUE.dequeue()
        if job:
            job_id, job_data = job
            process_job(job_id, job_data)
        else:
           
            time.sleep(random.randint(7, 15))

if __name__ == "__main__":
    main()
