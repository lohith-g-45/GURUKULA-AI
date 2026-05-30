
from typing import Dict, Any, List
from datetime import datetime
from app.services.data_loader import DataLoader
from app.schemas.tasks import Task
from app.database.task_store import task_store
from app.database.user_store import user_profile_store
from app.utils.logger import logger


class ReplanningAgent:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()

    def generate_replan(self, current_tasks: List[Task] = None, missed_tasks: List[str] = None, new_availability: float = None, readiness_change: float = None) -> Dict[str, Any]:
        try:
            if current_tasks is None:
                current_tasks = task_store.get_all_tasks()
            
            profile = user_profile_store.get_profile()
            planning_data = self.all_data.get("planning", {})
            rescheduling_rules = planning_data.get("adaptive_rescheduling_rules", {})
            recovery_rules = self.all_data.get("recommendations", {}).get("recovery_rules", {})

            adjustments = []
            recovered_tasks = []
            workload_balance = {}

            # Calculate actual missed tasks
            if missed_tasks is None:
                now = datetime.now()
                pending_tasks = [t for t in current_tasks if t.status == "pending"]
                missed_tasks = [
                    t.id for t in pending_tasks if hasattr(t, "due_date") and t.due_date < now.isoformat()]

            if missed_tasks:
                adjustments.append({
                    "type": "missed_task_recovery",
                    "tasks": missed_tasks,
                    "action": "Reschedule missed tasks with higher priority"
                })
                recovered_tasks = [{"task_id": t, "new_priority": "High"} for t in missed_tasks]

            if new_availability is None:
                new_availability = user_profile_store.get_available_hours()

            if new_availability:
                adjustments.append({
                    "type": "availability_change",
                    "new_hours": new_availability,
                    "action": "Adjust task durations and daily load"
                })
                
                # Calculate actual workload balance
                subject_workload = {}
                for task in current_tasks:
                    if task.status == "pending":
                        if task.subject not in subject_workload:
                            subject_workload[task.subject] = 0
                        subject_workload[task.subject] += task.estimated_hours or 0
                workload_balance = subject_workload

            if readiness_change is None:
                readiness_change = 0

            if readiness_change:
                adjustments.append({
                    "type": "readiness_change",
                    "change": readiness_change,
                    "action": "Adjust study intensity and focus areas"
                })

            return {
                "adjustments": adjustments,
                "recovered_tasks": recovered_tasks,
                "workload_balance": workload_balance,
                "rescheduling_rules": rescheduling_rules,
                "recovery_rules": recovery_rules,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating replan: {e}")
            return {
                "adjustments": [],
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }


replanning_agent = ReplanningAgent()
