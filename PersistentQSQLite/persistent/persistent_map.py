import abc
from typing import Any, Optional

class Persistent_map(abc.ABC):
    @abc.abstractmethod
    def enqueue(self, job_id: str, job_data: Any) :
        """Enqueue a job with a unique job_id and associated data."""
        pass

    @abc.abstractmethod
    def dequeue(self, consumer_id: str) :
        """Atomically dequeue a pending job for the specified consumer."""
        pass

    @abc.abstractmethod
    def update_job_status(self, job_id: str, status: str) :
        """Atomically update the status of a job."""
        pass

    @abc.abstractmethod
    def get_job_status(self, job_id: str) -> Optional[str]:
        """Retrieve the current status of a job."""
        pass

    @abc.abstractmethod
    def list_jobs(self) :
        """List all jobs with details (job_id, job_data, status, consumer_id)."""
        pass

    @abc.abstractmethod
    def delete_all(self) :
        """Delete all job records from the database."""
        pass

    @abc.abstractmethod
    def assign_job(self, job_id: str, consumer_id: str) :
        """Assign (or reassign) a job to the specified consumer."""
        pass

    @abc.abstractmethod
    def get_pending_jobs(self) :
        """Return a list of pending jobs."""
        pass

    @abc.abstractmethod
    def get_failed_jobs(self) :
        """Return a list of failed jobs."""
        pass
