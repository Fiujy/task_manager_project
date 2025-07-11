from datetime import datetime
from enum import Enum
import time
import uuid

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class Task:
    def __init__(self, title, description="", priority=Priority.MEDIUM):
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")
        
        if not isinstance(priority, Priority):
            raise TypeError("Priority must be a Priority enum")
        
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = Status.TODO
        self.created_at = datetime.now()
        self.completed_at = None
        self.project_id = None

    def mark_completed(self):
        self.status = Status.DONE
        self.completed_at = datetime.now()

    def update_priority(self, new_priority):
        if not isinstance(new_priority, Priority):
            raise TypeError("Priority must be a Priority enum")
        self.priority = new_priority

    def assign_to_project(self, project_id):
        self.project_id = project_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "project_id": self.project_id
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data["priority"])
        )
        task.id = data["id"]
        task.status = Status(data["status"])
        task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        task.project_id = data.get("project_id")
        return task