import abc
from typing import Any, List, Optional, Tuple

class Persistent_blueprint(abc.ABC):
    @abc.abstractmethod
    def enqueue(self, job_id: str, job_data: Any) :
        """Enqueue a job with a unique job_id and its associated data."""
        pass

    @abc.abstractmethod
    def dequeue(self) :
        """Dequeue a job for processing (using atomic transactions)."""
        pass

    @abc.abstractmethod
    def update_job_status(self, job_id: str, status: str) :
        """Update the status of a given job."""
        pass

    @abc.abstractmethod
    def get_job_status(self, job_id: str):
        """Retrieve the status of a job by its ID."""
        pass

    @abc.abstractmethod
    def list_jobs(self) -> List[Tuple[str, Any, str]]:
        """List all jobs with their statuses."""
        pass

if __name__ == "__main__" :
    p = Persistent_blueprint()
    p.enqueue()
