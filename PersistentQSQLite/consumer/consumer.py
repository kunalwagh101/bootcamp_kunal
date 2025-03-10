import time
import random
import os
from datetime import datetime
from persistent.persistentQSQLAlchemy  import PersistentQSQLAlchemy as PersistentQ

QUEUE = PersistentQ()
CONSUMER_ID = f"consumer_{os.getpid()}"

def process_job(job_id: str, job_data: str):
    """
    Process the job by reading the file, prepending a timestamp to each line  
    If an error occurs, a random failure is simulated for testing.
    """
    try:
        with open(job_data, "r") as f:
            lines = f.readlines()
        timestamp = datetime.now().isoformat()
        processed_lines = [f"{timestamp} {line}" for line in lines]
        with open(job_data, "w") as f:
            f.writelines(processed_lines)
        print(f"[{CONSUMER_ID}] Processed job: {job_id}")
        QUEUE.update_job_status(job_id, "completed")
    except Exception as e:
        print(f"[{CONSUMER_ID}] Error processing job {job_id}: {e}")
    
        if random.random() < 0.2:
            print(f"[{CONSUMER_ID}] Simulating consumer crash!")
            raise SystemExit("Consumer crashed!")
        else:
            QUEUE.update_job_status(job_id, "pending")
            print(f"[{CONSUMER_ID}] Job {job_id} requeued for retry.")

def main():
    """
    Continuously attempt to dequeue and process jobs with random delays.
    """
    while True:
        job = QUEUE.dequeue(CONSUMER_ID)
        if job:
            job_id, job_data = job
            process_job(job_id, job_data)
        else:
            time.sleep(random.randint(7, 15))

if __name__ == "__main__":
    main()
