import sqlite3
from typing import Any
from persistent.persistent_map import Persistent_blueprint
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


DB_FILE = "queue.db"
MAX_ATTEMPTS = 3      
TIMEOUT_SECONDS = 60  

class PersistentQSQLite(Persistent_blueprint):
    """
    A SQLite-based implementation of the persistent queue.
    """

    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._initialize_db()
        self.connection = sqlite3.connect(self.db_file)

    def _initialize_db(self):
        """
        Initialize the database by creating the jobs table if it does not exist.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                job_data TEXT,
                status TEXT,
                attempts INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                consumer_id TEXT DEFAULT NULL
            )
        """)
        conn.commit()
        conn.close()

    def enqueue(self, job_id: str, job_data: Any) -> None:
        """
        Enqueue a new job with a unique job_id and associated job_data.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO jobs (job_id, job_data, status, attempts, last_updated, consumer_id)
            VALUES (?, ?, 'pending', 0, CURRENT_TIMESTAMP, NULL)
        """, (job_id, str(job_data)))
        conn.commit()
        conn.close()

    def cleanup_stuck_jobs(self, timeout: int = TIMEOUT_SECONDS, max_attempts: int = MAX_ATTEMPTS) -> None:
        """
        Reset jobs that have been stuck in the 'processing' state beyond the specified timeout.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
   
        c.execute(f"""
            UPDATE jobs 
            SET status = 'pending', last_updated = CURRENT_TIMESTAMP, consumer_id = NULL 
            WHERE status = 'processing'
              AND last_updated < datetime('now', '-{timeout} seconds')
              AND attempts < ?
        """, (max_attempts,))

        c.execute(f"""
            UPDATE jobs 
            SET status = 'failed', last_updated = CURRENT_TIMESTAMP, consumer_id = NULL 
            WHERE status = 'processing'
              AND last_updated < datetime('now', '-{timeout} seconds')
              AND attempts >= ?
        """, (max_attempts,))
        conn.commit()
        conn.close()

    def dequeue(self, consumer_id: str):
        """
        Dequeue a pending job for a specific consumer.
        """
        self.cleanup_stuck_jobs()
        conn = sqlite3.connect(self.db_file)
        conn.isolation_level = None 
        c = conn.cursor()
        try:
            c.execute("BEGIN EXCLUSIVE")
            c.execute("SELECT job_id, job_data, attempts FROM jobs WHERE status = 'pending' LIMIT 1")
            row = c.fetchone()
            if row:
                job_id, job_data, attempts = row
                new_attempts = attempts + 1
                if new_attempts > MAX_ATTEMPTS:
                    c.execute("""
                        UPDATE jobs 
                        SET status = 'failed', attempts = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = ?
                        WHERE job_id = ?
                    """, (new_attempts, consumer_id, job_id))
                    conn.commit()
                    return None
                else:
                    c.execute("""
                        UPDATE jobs 
                        SET status = 'processing', attempts = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = ?
                        WHERE job_id = ?
                    """, (new_attempts, consumer_id, job_id))
                    conn.commit()
                    return job_id, job_data
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.exception(f"Error during dequeue for consumer {consumer_id}: {e}")
            raise e
        finally:
            conn.close()
        return None

    def update_job_status(self, job_id: str, status: str) -> None:
        """
        Update the status of a job.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        try:
            if status == 'completed':
                c.execute("""
                    UPDATE jobs 
                    SET status = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE job_id = ?
                """, (status, job_id))
            else:
                c.execute("""
                    UPDATE jobs 
                    SET status = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = NULL
                    WHERE job_id = ?
                """, (status, job_id))
            conn.commit()
        except Exception as e:
            logger.exception(f"Error updating job status for {job_id}: {e}")
        finally:
            conn.close()

    def get_job_status(self, job_id: str):
        """
        Retrieve the current status of a job identified by job_id.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def get_attempts(self, job_id: str):
        """
        Retrieve the number of attempts made for the job identified by job_id.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT attempts FROM jobs WHERE job_id = ?", (job_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else 0

    def list_jobs(self):
        """
        List all jobs in the persistent queue.
        """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT job_id, job_data, status, consumer_id FROM jobs")
        rows = c.fetchall()
        conn.close()
        return rows

    def get_all_failed_status(self):
        """
        Retrieve all jobs that have been marked as 'failed'.
        """
        c = self.connection.cursor()
        c.execute("SELECT * FROM jobs WHERE status = 'failed'")
        rows = c.fetchall()
        c.close()
        return rows

    def delete_all(self):
        """
        Delete all job records from the database.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("DELETE FROM jobs")
            return True
        except Exception as e:
            logger.exception(f"Error deleting all jobs: {e}")
            return False

    def assign_job(self, job_id: str, consumer_id: str):
        """
        Assign or reassign the specified job to a consumer.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                c = conn.cursor()
                c.execute("SELECT job_id FROM jobs WHERE job_id = ?", (job_id,))
                row = c.fetchone()
                if not row:
                    return False  
                c.execute("""
                    UPDATE jobs 
                    SET consumer_id = ?, status = 'processing', last_updated = CURRENT_TIMESTAMP 
                    WHERE job_id = ?
                """, (consumer_id, job_id))
                conn.commit()
            return True
        except Exception as e:
            logger.exception(f"Error assigning job {job_id} to consumer {consumer_id}: {e}")
            return False



# import sqlite3
# from typing import Any
# from persistent.persistent_map import Persistent_blueprint
# import logging


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)

# if not logger.handlers:
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

# DB_FILE = "queue.db"
# MAX_ATTEMPTS = 3      
# TIMEOUT_SECONDS = 60  



# class PersistentQSQLite(Persistent_blueprint):

#     def __init__(self, db_file: str = DB_FILE):
#         self.db_file = db_file
#         self._initialize_db()
#         self.connection = sqlite3.connect(self.db_file)

#     def _initialize_db(self):
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS jobs (
#                 job_id TEXT PRIMARY KEY,
#                 job_data TEXT,
#                 status TEXT,
#                 attempts INTEGER DEFAULT 0,
#                 last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 consumer_id TEXT DEFAULT NULL
#             )
#         """)
#         conn.commit()
#         conn.close()

#     def enqueue(self, job_id: str, job_data: Any) -> None:
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
#         c.execute("""
#             INSERT OR IGNORE INTO jobs (job_id, job_data, status, attempts, last_updated, consumer_id)
#             VALUES (?, ?, 'pending', 0, CURRENT_TIMESTAMP, NULL)
#         """, (job_id, str(job_data)))
#         conn.commit()
#         conn.close()

#     def cleanup_stuck_jobs(self, timeout: int = TIMEOUT_SECONDS, max_attempts: int = MAX_ATTEMPTS) -> None:
#         """
#         Reset jobs stuck in 'processing' state beyond the timeout..
#         """
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
    
#         c.execute(f"""
#             UPDATE jobs 
#             SET status = 'pending', last_updated = CURRENT_TIMESTAMP, consumer_id = NULL 
#             WHERE status = 'processing'
#               AND last_updated < datetime('now', '-{timeout} seconds')
#               AND attempts < ?
#         """, (max_attempts,))
    
#         c.execute(f"""
#             UPDATE jobs 
#             SET status = 'failed', last_updated = CURRENT_TIMESTAMP, consumer_id = NULL 
#             WHERE status = 'processing'
#               AND last_updated < datetime('now', '-{timeout} seconds')
#               AND attempts >= ?
#         """, (max_attempts,))
#         conn.commit()
#         conn.close()

#     def dequeue(self, consumer_id: str) :
     
#         self.cleanup_stuck_jobs()
#         conn = sqlite3.connect(self.db_file)
#         conn.isolation_level = None  
#         c = conn.cursor()
#         try:
#             c.execute("BEGIN EXCLUSIVE")
#             c.execute("SELECT job_id, job_data, attempts FROM jobs WHERE status = 'pending' LIMIT 1")
#             row = c.fetchone()
#             if row:
#                 job_id, job_data, attempts = row
#                 new_attempts = attempts + 1
#                 if new_attempts > MAX_ATTEMPTS:
                
#                     c.execute("""
#                         UPDATE jobs 
#                         SET status = 'failed', attempts = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = ?
#                         WHERE job_id = ?
#                     """, (new_attempts, consumer_id, job_id))
#                     conn.commit()
#                     return None
#                 else:
#                     c.execute("""
#                         UPDATE jobs 
#                         SET status = 'processing', attempts = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = ?
#                         WHERE job_id = ?
#                     """, (new_attempts, consumer_id, job_id))
#                     conn.commit()
#                     return job_id, job_data
#             conn.commit()
#         except Exception as e:
#             conn.rollback()
#             raise e
#         finally:
#             conn.close()
#         return None

#     def update_job_status(self, job_id: str, status: str) -> None:
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
      
#         if status == 'completed':
         
#             c.execute("""
#                 UPDATE jobs 
#                 SET status = ?, last_updated = CURRENT_TIMESTAMP
#                 WHERE job_id = ?
#             """, (status, job_id))
#         else:
           
#             c.execute("""
#                 UPDATE jobs 
#                 SET status = ?, last_updated = CURRENT_TIMESTAMP, consumer_id = NULL
#                 WHERE job_id = ?
#             """, (status, job_id))
#         conn.commit()
#         conn.close()

#     def get_job_status(self, job_id: str) :
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
#         c.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else None

#     def get_attempts(self, job_id: str) :
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
#         c.execute("SELECT attempts FROM jobs WHERE job_id = ?", (job_id,))
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else 0

#     def list_jobs(self) :
#         conn = sqlite3.connect(self.db_file)
#         c = conn.cursor()
#         c.execute("SELECT job_id, job_data, status ,consumer_id FROM jobs")
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_all_failed_status(self):
#         """
        
#         """

#         c   =  self.connection.cursor()
#         c.execute("SELECT * from jobs WHERE status = 'failed' ")
#         rows  = c.fetchall()
#         c.close()
#         return rows
    
#     def delete_all(self):
#         """
#         """
#         try : 
#             conn = sqlite3.connect(self.db_file)
#             c = conn.cursor()
#             c.execute("DELETE FROM jobs")
#             conn.commit()
#             conn.close()
#             return True
#         except Exception as e:
#             return False


#     def assign_job(self, job_id: str, consumer_id: str) :
#         """
#         Assign or reassign the specified job to a consumer.     
#         """
#         try:
#             with sqlite3.connect(self.db_file) as conn:
#                 c = conn.cursor()
#                 c.execute("SELECT job_id FROM jobs WHERE job_id = ?", (job_id,))
#                 row = c.fetchone()
#                 if not row:
#                     return False  
#                 c.execute("""
#                     UPDATE jobs 
#                     SET consumer_id = ?, status = 'processing', last_updated = CURRENT_TIMESTAMP 
#                     WHERE job_id = ?
#                 """, (consumer_id, job_id))
#                 conn.commit()
#             return True
#         except Exception as e :
#             logger.exception(f"Error assigning job {job_id} to consumer {consumer_id}: {e}")
#             return False



if __name__ =="__main__" :
    p = PersistentQSQLite()
    print(p.enqueue("/mnt/h/Aganitha/bootcamp/PersistentQSQLite/job_1740397874_khiwz.txt","/mnt/h/Aganitha/bootcamp/PersistentQSQLite/job_1740397874_khiwz.txt"))
    print(p.get_job_status("/mnt/h/Aganitha/bootcamp/PersistentQSQLite/job_1740397874_khiwz.txt"))

