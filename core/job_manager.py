import threading
import uuid
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timezone

from core.logger import get_logger, get_system_resources
from core.task_status import JobStatus

logger = get_logger("JobManager")

class Job:
    def __init__(self, job_id: str, name: str, target: Callable, args=(), kwargs=None):
        self.job_id = job_id
        self.name = name
        self.target = target
        self.args = args
        self.kwargs = kwargs or {}
        self.status = JobStatus.PENDING
        self.progress = 0
        self.message = "Job initialized"
        self.result = None
        self.error = None
        self.started_at = None
        self.finished_at = None
        self.thread: Optional[threading.Thread] = None

    def run(self):
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now(timezone.utc).isoformat()
        logger.info(f"Starting job [{self.name}] ({self.job_id})")
        try:
            self.result = self.target(self, *self.args, **self.kwargs)
            self.status = JobStatus.COMPLETED
            self.progress = 100
            self.message = "Job completed successfully"
            logger.info(f"Job [{self.name}] completed successfully")
        except Exception as e:
            self.status = JobStatus.FAILED
            self.error = str(e)
            self.message = f"Failed: {e}"
            logger.error(f"Job [{self.name}] failed: {e}", exc_info=True)
        finally:
            self.finished_at = datetime.now(timezone.utc).isoformat()

    def set_progress(self, percent: int, message: str = ""):
        self.progress = max(0, min(100, percent))
        if message:
            self.message = message
        logger.debug(f"Job [{self.name}] {self.progress}%: {self.message}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "name": self.name,
            "status": self.status.value if hasattr(self.status, 'value') else str(self.status),
            "progress": self.progress,
            "message": self.message,
            "error": self.error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "resources": get_system_resources()
        }

class JobManager:
    """Singleton job runner enforcing single-worker sequential execution for 8 GB RAM safety."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(JobManager, cls).__new__(cls)
                cls._instance.jobs: Dict[str, Job] = {}
                cls._instance._render_lock = threading.Lock()
        return cls._instance

    def is_render_active(self) -> bool:
        with self._lock:
            for j in self.jobs.values():
                if j.status == JobStatus.RUNNING and ("render" in j.name.lower() or "production" in j.name.lower()):
                    return True
            return False

    def submit_job(self, name: str, target: Callable, *args, **kwargs) -> str:
        job_id = str(uuid.uuid4())[:8]
        job = Job(job_id, name, target, args=args, kwargs=kwargs)
        
        with self._lock:
            self.jobs[job_id] = job

        thread = threading.Thread(target=job.run, daemon=True)
        job.thread = thread
        thread.start()
        return job_id

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            j = self.jobs.get(job_id)
            return j.to_dict() if j else None

    def list_jobs(self) -> Dict[str, Any]:
        with self._lock:
            return {jid: j.to_dict() for jid, j in self.jobs.items()}

def get_job_manager() -> JobManager:
    return JobManager()
