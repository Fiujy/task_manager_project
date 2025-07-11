import smtplib
import csv
from datetime import datetime
import re

class EmailService:
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        self.smtp_server = smtp_server
        self.port = port

    def send_task_reminder(self, email, task_title, due_date):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email address")
        
        # Je simule l'envoi d'email avec un print
        print(f"Sending reminder to {email} for task: {task_title}")
        return True

    def send_completion_notification(self, email, task_title):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email address")
        
        # Je simule l'envoi d'email avec un print
        print(f"Sending completion notification to {email} for task: {task_title}")
        return True

    def _is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class ReportService:
    def generate_daily_report(self, tasks, date=None):
        if date is None:
            date = datetime.now()
        
        daily_tasks = [task for task in tasks if task.created_at.date() == date.date()]
        completed_today = [task for task in daily_tasks if task.status.value == "done"]
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "total_tasks_created": len(daily_tasks),
            "tasks_completed": len(completed_today),
            "completion_rate": len(completed_today) / len(daily_tasks) * 100 if daily_tasks else 0
        }

    def export_tasks_csv(self, tasks, filename):
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Title', 'Description', 'Priority', 'Status', 'Created', 'Completed'])
                
                for task in tasks:
                    writer.writerow([
                        task.id,
                        task.title,
                        task.description,
                        task.priority.value,
                        task.status.value,
                        task.created_at.isoformat(),
                        task.completed_at.isoformat() if task.completed_at else ""
                    ])
        except IOError as e:
            raise IOError(f"Failed to export CSV: {e}")