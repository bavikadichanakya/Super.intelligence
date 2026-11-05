import threading
import uuid
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime

from core.logger import get_logger, get_system_resources

logger = get_logger("TaskManager")

class Task:
    def __init__(self, task_id: str, name: str, target: Callable, args=(), kwargs=None):
        self.task_id = task_id
        self.name = name
        self.target = target
        self.args = args
        self.kwargs = kwargs or {}
        self.status = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
        self.progress = 0  # 0 to 100
        self.message = "Task initialized"
        self.result = None
        self.error = None
        self.started_at = None
        self.finished_at = None
        self.thread: Optional[threading.Thread] = None

    def run(self):
        self.status = "RUNNING"
        self.started_at = datetime.utcnow().isoformat()
        logger.info(f"Starting task [{self.name}] ({self.task_id})")
        try:
            self.result = self.target(self, *self.args, **self.kwargs)
            self.status = "COMPLETED"
            self.progress = 100
            self.message = "Task completed successfully"
            logger.info(f"Task [{self.name}] completed successfully")
        except Exception as e:
            self.status = "FAILED"
            self.error = str(e)
            self.message = f"Failed: {e}"
            logger.error(f"Task [{self.name}] failed with error: {e}", exc_info=True)
        finally:
            self.finished_at = datetime.utcnow().isoformat()

    def set_progress(self, percent: int, message: str = ""):
        self.progress = max(0, min(100, percent))
        if message:
            self.message = message
        logger.debug(f"Task [{self.name}] progress: {self.progress}% - {self.message}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "error": self.error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "system_resources": get_system_resources()
        }

class TaskManager:
    """Singleton task manager for executing asynchronous long-running operations."""
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TaskManager, cls).__new__(cls)
                cls._instance.tasks: Dict[str, Task] = {}
        return cls._instance

    def submit_task(self, name: str, target: Callable, *args, **kwargs) -> str:
        task_id = str(uuid.uuid4())[:8]
        task = Task(task_id, name, target, args=args, kwargs=kwargs)
        
        with self._lock:
            self.tasks[task_id] = task

        thread = threading.Thread(target=task.run, daemon=True)
        task.thread = thread
        thread.start()
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            task = self.tasks.get(task_id)
            return task.to_dict() if task else None

    def list_tasks(self) -> Dict[str, Any]:
        with self._lock:
            return {tid: t.to_dict() for tid, t in self.tasks.items()}

    def is_render_running(self) -> bool:
        """Check if any rendering task is currently in progress (enforces sequential rendering)."""
        with self._lock:
            for task in self.tasks.values():
                if task.status == "RUNNING" and "render" in task.name.lower():
                    return True
        return False

def get_task_manager() -> TaskManager:
    return TaskManager()
