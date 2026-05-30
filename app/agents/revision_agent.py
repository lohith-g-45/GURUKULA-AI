
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.services.data_loader import DataLoader
from app.database.user_store import user_profile_store
from app.database.task_store import task_store
from app.utils.logger import logger


class RevisionAgent:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()

    def generate_revision_schedule(self, subject: str = None, recent_tasks: List[str] = None, current_readiness: float = None) -> Dict[str, Any]:
        try:
            profile = user_profile_store.get_profile()
            if current_readiness is None:
                current_readiness = user_profile_store.get_readiness_score()
            
            weak_subjects = user_profile_store.get_weak_subjects()
            
            planning_data = self.all_data.get("planning", {})
            revision_data = planning_data.get("revision_cycles", {})
            recovery_rules = self.all_data.get("recommendations", {}).get("recovery_rules", {})

            spaced_intervals = revision_data.get("spaced_repetition_intervals", [1, 3, 7, 14])
            subject_priorities = revision_data.get("subject_revision_priority", {})

            if subject:
                subjects = [subject]
            elif weak_subjects:
                subjects = weak_subjects
            else:
                subjects = list(subject_priorities.keys())

            revision_tasks = []

            for subj in subjects:
                priority_info = subject_priorities.get(subj, {"priority_score": 5, "revision_frequency": "weekly"})
                # Adjust intervals based on readiness
                adjusted_intervals = [
                    max(1, int(i * (current_readiness / 70))) 
                    for i in spaced_intervals
                ]
                
                for interval in adjusted_intervals:
                    revision_date = datetime.now() + timedelta(days=interval)
                    revision_tasks.append({
                        "subject": subj,
                        "revision_date": revision_date.isoformat(),
                        "interval_days": interval,
                        "priority_score": priority_info.get("priority_score", 8) if subj in weak_subjects else priority_info.get("priority_score", 5),
                        "revision_frequency": priority_info.get("revision_frequency", "weekly"),
                        "type": "spaced_repetition"
                    })

            # Recovery suggestions based on actual weak subjects
            recovery_suggestions = recovery_rules.copy()
            if weak_subjects:
                recovery_suggestions["urgent_review"] = weak_subjects[:3]

            return {
                "revision_tasks": revision_tasks,
                "spaced_repetition_intervals": spaced_intervals,
                "subject_priorities": subject_priorities,
                "recovery_suggestions": recovery_suggestions,
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
