import pytest
from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status

class TestTaskManagerBasics:
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")

    def test_add_task_returns_id(self):
        task_id = self.manager.add_task("Test task")
        assert task_id is not None
        assert len(self.manager.tasks) == 1
        assert self.manager.tasks[0].title == "Test task"

    def test_get_task_existing(self):
        task_id = self.manager.add_task("Test task", "Description", Priority.HIGH)
        task = self.manager.get_task(task_id)
        
        assert task is not None
        assert task.title == "Test task"
        assert task.description == "Description"
        assert task.priority == Priority.HIGH

    def test_get_task_nonexistent_returns_none(self):
        task = self.manager.get_task("nonexistent_id")
        assert task is None

    def test_delete_task_existing(self):
        task_id = self.manager.add_task("Test task")
        result = self.manager.delete_task(task_id)
        assert result is True
        assert len(self.manager.tasks) == 0

    def test_delete_task_nonexistent(self):
        result = self.manager.delete_task("nonexistent_id")
        assert result is False

class TestTaskManagerFiltering:
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        self.manager.add_task("Task 1", "Desc 1", Priority.HIGH)
        self.manager.add_task("Task 2", "Desc 2", Priority.LOW)
        self.manager.add_task("Task 3", "Desc 3", Priority.HIGH)
        self.manager.tasks[1].mark_completed()

    def test_get_tasks_by_status(self):
        todo_tasks = self.manager.get_tasks_by_status(Status.TODO)
        done_tasks = self.manager.get_tasks_by_status(Status.DONE)
        
        assert len(todo_tasks) == 2
        assert len(done_tasks) == 1
        assert done_tasks[0].title == "Task 2"

    def test_get_tasks_by_priority(self):
        high_tasks = self.manager.get_tasks_by_priority(Priority.HIGH)
        low_tasks = self.manager.get_tasks_by_priority(Priority.LOW)
        
        assert len(high_tasks) == 2
        assert len(low_tasks) == 1
        assert low_tasks[0].title == "Task 2"

    def test_get_statistics(self):
        stats = self.manager.get_statistics()
        
        assert stats["total_tasks"] == 3
        assert stats["completed_tasks"] == 1
        assert stats["tasks_by_priority"]["high"] == 2
        assert stats["tasks_by_priority"]["low"] == 1
        assert stats["tasks_by_status"]["todo"] == 2
        assert stats["tasks_by_status"]["done"] == 1

class TestTaskManagerPersistence:
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        self.manager.add_task("Task 1", "Desc 1", Priority.HIGH)
        self.manager.add_task("Task 2", "Desc 2", Priority.LOW)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        self.manager.save_to_file()
        
        mock_file.assert_called_once_with("test_tasks.json", 'w')
        mock_json_dump.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": "1", "title": "Test", "description": "", "priority": "medium", "status": "todo", "created_at": "2023-01-01T00:00:00", "completed_at": null, "project_id": null}]')
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file):
        mock_json_load.return_value = [{
            "id": "1",
            "title": "Test",
            "description": "",
            "priority": "medium",
            "status": "todo",
            "created_at": "2023-01-01T00:00:00",
            "completed_at": None,
            "project_id": None
        }]
        
        self.manager.load_from_file()
        
        mock_file.assert_called_once_with("test_tasks.json", 'r')
        assert len(self.manager.tasks) == 1
        assert self.manager.tasks[0].title == "Test"

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        self.manager.load_from_file()
        assert len(self.manager.tasks) == 0

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_save_to_file_error(self, mock_file):
        with pytest.raises(IOError):
            self.manager.save_to_file()