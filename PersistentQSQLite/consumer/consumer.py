import time
import random
import os
from datetime import datetime
from persistent import get_queue
from persistent.persistent_queue import MAX_ATTEMPTS

QUEUE = get_queue()

CONSUMER_ID = f"consumer_{os.getpid()}"

def process_job(job_id: str, job_data: str):
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
        current_attempts = QUEUE.get_attempts(job_id)
        if current_attempts >= MAX_ATTEMPTS:
            QUEUE.update_job_status(job_id, "failed")
            print(f"[{CONSUMER_ID}] Job {job_id} marked as failed after {current_attempts} attempts.")
        else:
            QUEUE.update_job_status(job_id, "pending")
            print(f"[{CONSUMER_ID}] Job {job_id} requeued for retry (attempt {current_attempts}).")

def main():
    while True:
        job = QUEUE.dequeue(CONSUMER_ID)
        if job:
            job_id, job_data = job
            process_job(job_id, job_data)
        else:
            time.sleep(random.randint(7, 15))

if __name__ == "__main__":
    main()
