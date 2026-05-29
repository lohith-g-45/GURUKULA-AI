
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.services.data_loader import DataLoader
from app.utils.logger import logger


class RevisionAgent:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()

    def generate_revision_schedule(self, subject: str = None, recent_tasks: List[str] = None, current_readiness: float = 70.0) -> Dict[str, Any]:
        try:
            planning_data = self.all_data.get("planning", {})
            revision_data = planning_data.get("revision_cycles", {})
            recovery_rules = self.all_data.get("recommendations", {}).get("recovery_rules", {})

            spaced_intervals = revision_data.get("spaced_repetition_intervals", [1, 3, 7, 14])
            subject_priorities = revision_data.get("subject_revision_priority", {})

            subjects = [subject] if subject else list(subject_priorities.keys())
            revision_tasks = []

            for subj in subjects:
                priority_info = subject_priorities.get(subj, {"priority_score": 5, "revision_frequency": "weekly"})
                for interval in spaced_intervals:
                    revision_date = datetime.now() + timedelta(days=interval)
                    revision_tasks.append({
                        "subject": subj,
                        "revision_date": revision_date.isoformat(),
                        "interval_days": interval,
                        "priority_score": priority_info.get("priority_score"),
                        "revision_frequency": priority_info.get("revision_frequency"),
                        "type": "spaced_repetition"
                    })

            return {
                "revision_tasks": revision_tasks,
                "spaced_repetition_intervals": spaced_intervals,
                "subject_priorities": subject_priorities,
                "recovery_suggestions": recovery_rules,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating revision schedule: {e}")
            return {
                "revision_tasks": [],
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }


revision_agent = RevisionAgent()
