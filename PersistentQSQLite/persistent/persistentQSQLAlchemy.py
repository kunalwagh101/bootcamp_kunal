import os
import datetime
import logging
from typing import Any, List, Optional, Tuple
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from persistent.persistent_map import Persistent_map  
from dotenv import load_dotenv


load_dotenv()


DB_FILE = os.getenv("QUEUE_DB_FILE", "queue.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "3"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "60"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(String, primary_key=True, index=True)
    job_data = Column(String)
    status = Column(String, default="pending")
    attempts = Column(Integer, default=0)
    last_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    consumer_id = Column(String, nullable=True) 
    last_consumer = Column(String, nullable=True)  

    def __repr__(self):
        return f"<Job(job_id={self.job_id}, status={self.status}, attempts={self.attempts}, consumer_id={self.consumer_id}, last_consumer={self.last_consumer})>"

class PersistentQSQLAlchemy(Persistent_map):
    """
    SQLAlchemy-based implementation of the persistent queue.
    """

    def __init__(self):
        """Initialize the persistent queue and create the database tables if they do not exist."""
        Base.metadata.create_all(bind=engine)

    def enqueue(self, job_id: str, job_data: Any) :
        """
        Enqueue a new job with the specified job_id and job_data.      
        The job is inserted with a default status of 'pending'.
        """
        session = SessionLocal()
        try:
            job = Job(job_id=job_id, job_data=str(job_data), status="pending")
            session.add(job)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error enqueuing job {job_id}: {e}")
        finally:
            session.close()

    def cleanup_stuck_jobs(self) :
        """
        Reset jobs stuck in 'processing' beyond TIMEOUT_SECONDS.       
        If a job's attempts are less than MAX_ATTEMPTS, it is requeued (status set to 'pending');
        otherwise, it is marked as 'failed'. The consumer_id is cleared.
        """
        session = SessionLocal()
        try:
            cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=TIMEOUT_SECONDS)
            stuck_jobs = session.query(Job).filter(Job.status == "processing", Job.last_updated < cutoff).all()
            for job in stuck_jobs:
                if job.attempts < MAX_ATTEMPTS:
                    job.status = "pending"
                    job.consumer_id = None
                    job.last_updated = datetime.datetime.now(datetime.timezone.utc)
                else:
                    job.status = "failed"
                    job.consumer_id = None
                    job.last_updated = datetime.datetime.now(datetime.timezone.utc)
    
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error cleaning up stuck jobs: {e}")
        finally:
            session.close()

    def dequeue(self, consumer_id: str) -> Optional[Tuple[str, Any]]:
        """
        Atomically dequeue a pending job for the specified consumer.      
        Increments the attempt count; if the count exceeds MAX_ATTEMPTS, marks the job as 'failed'.
        Otherwise, assigns the job to the consumer and updates its status to 'processing'.
        """
        self.cleanup_stuck_jobs()
        session = SessionLocal()
        try:
            session.begin()
            job = session.query(Job).filter(Job.status == "pending").with_for_update(nowait=True).first()
            if job:
                job.attempts += 1
                if job.attempts > MAX_ATTEMPTS:
                    job.status = "failed"
                    job.consumer_id = consumer_id
                    job.last_consumer = consumer_id
                    session.commit()
                    return None
                else:
                    job.status = "processing"
                    job.consumer_id = consumer_id
                    job.last_updated = datetime.datetime.now(datetime.timezone.utc)
                    session.commit()
                    return job.job_id, job.job_data
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error during dequeue for consumer {consumer_id}: {e}")
            raise e
        finally:
            session.close()

    def update_job_status(self, job_id: str, status: str):
        """
        Atomically update the status of the job with the given job_id.
        If the new status is not 'processing', clears the consumer_id and saves it as last_consumer.
        Uses timezone-aware datetime for last_updated.
        """
        session = SessionLocal()
        try:
            job = session.query(Job).filter(Job.job_id == job_id).first()
            if job:
                job.status = status
                if status != "processing":
                    job.last_consumer = job.consumer_id
                    job.consumer_id = None
                job.last_updated = datetime.datetime.now(datetime.timezone.utc)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error updating job status for {job_id}: {e}")
        finally:
            session.close()

    def get_job_status(self, job_id: str) :
        """
        Retrieve the current status of the job with the given job_id.
        """
        session = SessionLocal()
        try:
            job = session.query(Job).filter(Job.job_id == job_id).first()
            return job.status if job else None
        except SQLAlchemyError as e:
            logger.exception(f"Error retrieving job status for {job_id}: {e}")
            return None
        finally:
            session.close()

    def list_jobs(self) :
        """
        List all jobs in the persistent queue.
        """
        session = SessionLocal()
        try:
            jobs = session.query(Job).all()
            return [(job.job_id, job.job_data, job.status, job.consumer_id, job.last_consumer) for job in jobs]
        except SQLAlchemyError as e:
            logger.exception(f"Error listing jobs: {e}")
            return []
        finally: 
            session.close()

    def get_pending_jobs(self) :
        """
        Retrieve all pending jobs.
        """
        session = SessionLocal()
        try:
            jobs = session.query(Job).filter(Job.status == "pending").all()
            return [(job.job_id, job.job_data) for job in jobs]
        except SQLAlchemyError as e:
            logger.exception(f"Error retrieving pending jobs: {e}")
            return []
        finally:
            session.close()

    def get_failed_jobs(self) :
        """
        Retrieve all failed jobs.
        """
        session = SessionLocal()
        try:
            jobs = session.query(Job).filter(Job.status == "failed").all()
            return [(job.job_id, job.job_data) for job in jobs]
        except SQLAlchemyError as e:
            logger.exception(f"Error retrieving failed jobs: {e}")
            return []
        finally:
            session.close()

    def delete_all(self) :
        """
        Delete all job records from the database.    
        """
        session = SessionLocal()
        try:
            session.query(Job).delete()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error deleting all jobs: {e}")
            return False
        finally:
            session.close()

    def assign_job(self, job_id: str, consumer_id: str) :
        """
        Assign (or reassign) the specified job to a consumer.     
        Sets the job's consumer_id, marks its status as 'processing', and updates last_updated. 
        """
        session = SessionLocal()
        try:
            job = session.query(Job).filter(Job.job_id == job_id).first()
            if not job:
                return False
            job.consumer_id = consumer_id
            job.status = "processing"
            job.last_updated = datetime.datetime.now(datetime.timezone.utc)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"Error assigning job {job_id} to consumer {consumer_id}: {e}")
            return False
        finally:
            session.close()


PersistentQSQLAlchemy = PersistentQSQLAlchemy
