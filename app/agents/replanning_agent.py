
from typing import Dict, Any, List
from datetime import datetime
from app.services.data_loader import DataLoader
from app.schemas.tasks import Task
from app.utils.logger import logger


class ReplanningAgent:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()

    def generate_replan(self, current_tasks: List[Task] = None, missed_tasks: List[str] = None, new_availability: float = None, readiness_change: float = None) -> Dict[str, Any]:
        try:
            planning_data = self.all_data.get("planning", {})
            rescheduling_rules = planning_data.get("adaptive_rescheduling_rules", {})
            recovery_rules = self.all_data.get("recommendations", {}).get("recovery_rules", {})

            adjustments = []
            recovered_tasks = []
            workload_balance = {}

            if missed_tasks:
                adjustments.append({
                    "type": "missed_task_recovery",
                    "tasks": missed_tasks,
                    "action": "Reschedule missed tasks with higher priority"
                })
                recovered_tasks = [{"task_id": t, "new_priority": "High"} for t in missed_tasks]

            if new_availability:
                adjustments.append({
                    "type": "availability_change",
                    "new_hours": new_availability,
                    "action": "Adjust task durations and daily load"
                })

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
