
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.services.data_loader import DataLoader
from app.schemas.tasks import TaskCreate, Task
from app.database.task_store import task_store
from app.database.user_store import user_profile_store
from app.utils.logger import logger


class TaskGenerationEngine:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()

    def generate_initial_tasks(self) -> List[Task]:
        logger.info("Generating initial tasks")
        profile = user_profile_store.get_profile()
        weak_subjects = user_profile_store.get_weak_subjects()
        available_hours = user_profile_store.get_available_hours()
        exam = user_profile_store.get_exam()
        planning_data = self.all_data.get('planning', {})
        subject_priority = planning_data.get('study_planning_rules', {}).get('daily_study_distribution_rules', {}).get('subject_priority_order', [])

        tasks = []

        daily_tasks = self._generate_daily_tasks(subject_priority, available_hours, weak_subjects)
        weekly_tasks = self._generate_weekly_tasks(subject_priority)
        revision_tasks = self._generate_revision_tasks(weak_subjects)
        mock_tasks = self._generate_mock_tasks(exam)

        all_task_dicts = daily_tasks + weekly_tasks + revision_tasks + mock_tasks
        for task_dict in all_task_dicts:
            task = task_store.create_task(TaskCreate(**task_dict))
            tasks.append(task)

        logger.info(f"Generated {len(tasks)} initial tasks")
        return tasks

    def _generate_daily_tasks(self, subjects: List[str], available_hours: float, weak_subjects: List[str]) -> List[Dict[str, Any]]:
        daily_tasks = []
        now = datetime.now()
        for i, subject in enumerate(subjects[:4]):
            priority = "High" if subject in weak_subjects else "Medium"
            duration = available_hours / 4
            task = {
                "title": f"Study {subject} Foundations",
                "description": f"Complete daily study session for {subject}",
                "subject": subject,
                "priority": priority,
                "estimated_hours": duration,
                "due_date": (now + timedelta(days=1)).isoformat()
            }
            daily_tasks.append(task)
        return daily_tasks

    def _generate_weekly_tasks(self, subjects: List[str]) -> List[Dict[str, Any]]:
        weekly_tasks = []
        now = datetime.now()
        for subject in subjects[:3]:
            task = {
                "title": f"Weekly {subject} Review",
                "description": f"Complete weekly review and practice for {subject}",
                "subject": subject,
                "priority": "Medium",
                "estimated_hours": 2,
                "due_date": (now + timedelta(days=7)).isoformat()
            }
            weekly_tasks.append(task)
        return weekly_tasks

    def _generate_revision_tasks(self, weak_subjects: List[str]) -> List[Dict[str, Any]]:
        revision_tasks = []
        now = datetime.now()
        for subject in weak_subjects:
            for interval in [2, 7, 14]:
                task = {
                    "title": f"Spaced Revision: {subject}",
                    "description": f"Review {subject} topics for long-term retention",
                    "subject": subject,
                    "priority": "High",
                    "estimated_hours": 1.5,
                    "due_date": (now + timedelta(days=interval)).isoformat()
                }
                revision_tasks.append(task)
        return revision_tasks

    def _generate_mock_tasks(self, exam: str) -> List[Dict[str, Any]]:
        mock_tasks = []
        now = datetime.now()
        for i in range(1, 4):
            task = {
                "title": f"Mock Test {i} - {exam}",
                "description": f"Complete full-length {exam} mock test {i}",
                "subject": "Mock Test",
                "priority": "High",
                "estimated_hours": 3,
                "due_date": (now + timedelta(days=i*7)).isoformat()
            }
            mock_tasks.append(task)
        return mock_tasks


task_generation_engine = TaskGenerationEngine()

