import pytest
from unittest.mock import patch, Mock, mock_open
from datetime import datetime
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority, Status

class TestEmailService:
    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = self.email_service.send_task_reminder("user@example.com", "Test Task", datetime.now())
        assert result is True

    def test_send_task_reminder_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_task_reminder("invalid-email", "Test Task", datetime.now())

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_completion_notification_success(self, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = self.email_service.send_completion_notification("user@example.com", "Test Task")
        assert result is True

    def test_send_completion_notification_invalid_email(self):
        with pytest.raises(ValueError):
            self.email_service.send_completion_notification("invalid-email", "Test Task")

class TestReportService:
    def setup_method(self):
        self.report_service = ReportService()
        
        # Create test tasks
        self.task1 = Task("Task 1", "Description 1", Priority.HIGH)
        self.task2 = Task("Task 2", "Description 2", Priority.LOW)
        self.task2.mark_completed()
        self.tasks = [self.task1, self.task2]

    @patch('src.task_manager.services.datetime')
    def test_generate_daily_report_fixed_date(self, mock_datetime):
        fixed_date = datetime(2023, 1, 1)
        mock_datetime.now.return_value = fixed_date
        
        # Set task creation dates to match
        self.task1.created_at = fixed_date
        self.task2.created_at = fixed_date
        
        report = self.report_service.generate_daily_report(self.tasks, fixed_date)
        
        assert report["date"] == "2023-01-01"
        assert report["total_tasks_created"] == 2
        assert report["tasks_completed"] == 1
        assert report["completion_rate"] == 50.0

    def test_generate_daily_report_no_tasks(self):
        report = self.report_service.generate_daily_report([], datetime.now())
        
        assert report["total_tasks_created"] == 0
        assert report["tasks_completed"] == 0
        assert report["completion_rate"] == 0

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.task_manager.services.csv.writer')
    def test_export_tasks_csv(self, mock_writer, mock_file):
        mock_csv_writer = Mock()
        mock_writer.return_value = mock_csv_writer
        
        self.report_service.export_tasks_csv(self.tasks, "test.csv")
        
        mock_file.assert_called_once_with("test.csv", 'w', newline='')
        mock_csv_writer.writerow.assert_called()

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_export_tasks_csv_error(self, mock_file):
        with pytest.raises(IOError):
            self.report_service.export_tasks_csv(self.tasks, "test.csv")