import json
from typing import List, Optional
from .task import Task, Priority, Status

class TaskManager:
    def __init__(self, storage_file="tasks.json"):
        self.tasks = []
        self.storage_file = storage_file

    def add_task(self, title, description="", priority=Priority.MEDIUM):
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task.id

    def get_task(self, task_id) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority]

    def delete_task(self, task_id) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def save_to_file(self, filename=None):
        if filename is None:
            filename = self.storage_file
        
        try:
            with open(filename, 'w') as f:
                data = [task.to_dict() for task in self.tasks]
                json.dump(data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save tasks: {e}")

    def load_from_file(self, filename=None):
        if filename is None:
            filename = self.storage_file
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []
        except (json.JSONDecodeError, IOError) as e:
            raise IOError(f"Failed to load tasks: {e}")

    def get_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = len(self.get_tasks_by_status(Status.DONE))
        
        tasks_by_priority = {}
        for priority in Priority:
            tasks_by_priority[priority.value] = len(self.get_tasks_by_priority(priority))
        
        tasks_by_status = {}
        for status in Status:
            tasks_by_status[status.value] = len(self.get_tasks_by_status(status))
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "tasks_by_priority": tasks_by_priority,
            "tasks_by_status": tasks_by_status
        }