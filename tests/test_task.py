import pytest
from datetime import datetime
from src.task_manager.task import Task, Priority, Status

class TestTaskCreation:
    def test_create_task_minimal(self):
        task = Task("Test task")
        assert task.title == "Test task"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert task.status == Status.TODO
        assert task.created_at is not None
        assert task.completed_at is None
        assert task.project_id is None
        assert task.id is not None

    def test_create_task_complete(self):
        task = Task("Test task", "Test description", Priority.HIGH)
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO

    def test_create_task_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            Task("")

    def test_create_task_invalid_priority_raises_error(self):
        with pytest.raises(TypeError):
            Task("Test", priority="invalid")

class TestTaskOperations:
    def setup_method(self):
        self.task = Task("Test task", "Test description", Priority.MEDIUM)

    def test_mark_completed_changes_status(self):
        self.task.mark_completed()
        assert self.task.status == Status.DONE
        assert self.task.completed_at is not None

    def test_update_priority_valid(self):
        self.task.update_priority(Priority.HIGH)
        assert self.task.priority == Priority.HIGH

    def test_update_priority_invalid(self):
        with pytest.raises(TypeError):
            self.task.update_priority("invalid")

    def test_assign_to_project(self):
        self.task.assign_to_project("project_123")
        assert self.task.project_id == "project_123"

class TestTaskSerialization:
    def setup_method(self):
        self.task = Task("Test task", "Test description", Priority.HIGH)
        self.task.mark_completed()
        self.task.assign_to_project("project_123")

    def test_to_dict_contains_all_fields(self):
        data = self.task.to_dict()
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "priority" in data
        assert "status" in data
        assert "created_at" in data
        assert "completed_at" in data
        assert "project_id" in data
        assert isinstance(data["priority"], str)
        assert isinstance(data["status"], str)

    def test_from_dict_recreates_task(self):
        data = self.task.to_dict()
        new_task = Task.from_dict(data)
        
        assert new_task.id == self.task.id
        assert new_task.title == self.task.title
        assert new_task.description == self.task.description
        assert new_task.priority == self.task.priority
        assert new_task.status == self.task.status
        assert new_task.project_id == self.task.project_id