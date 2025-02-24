import sqlite3
from typing import Any, List, Optional, Tuple
from persistent.persistent_map import Persistent_blueprint

DB_FILE = "queue.db"

class PersistentQSQLite(Persistent_blueprint):
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._initialize_db()

    def _initialize_db(self):
        connection = sqlite3.connect(self.db_file)
        c = connection.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                job_data TEXT,
                status TEXT
            )
        """)
        connection.commit()
        connection.close()

    def enqueue(self, job_id: str, job_data: Any) :
        connection = sqlite3.connect(self.db_file)
        try:
            c = connection.cursor()
            c.execute("BEGIN IMMEDIATE")
            c.execute("INSERT OR IGNORE INTO jobs (job_id, job_data, status) VALUES (?, ?, ?)",
                      (job_id, str(job_data), "pending"))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def dequeue(self) :
        connection = sqlite3.connect(self.db_file)
        try:
            c = connection.cursor()
            c.execute("BEGIN IMMEDIATE")
            c.execute("SELECT job_id, job_data FROM jobs WHERE status = 'pending' LIMIT 1")
            row = c.fetchone()
            if row:
                job_id, job_data = row
                c.execute("UPDATE jobs SET status = 'processing' WHERE job_id = ?", (job_id,))
                connection.commit()
                return job_id, job_data
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
        return None

    def update_job_status(self, job_id: str, status: str):
        connection = sqlite3.connect(self.db_file)
        try:
            c = connection.cursor()
            c.execute("BEGIN IMMEDIATE")
            c.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def get_job_status(self, job_id: str) -> Optional[str]:
        connection = sqlite3.connect(self.db_file)
        try:
            c = connection.cursor()
            c.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
            row = c.fetchone()
        finally:
            connection.close()
        return row[0] if row else None

    def list_jobs(self) :
        connection = sqlite3.connect(self.db_file)
        try:
            c = connection.cursor()
            c.execute("SELECT job_id, job_data, status FROM jobs")
            rows = c.fetchall()
        finally:
            connection.close()
        return rows
