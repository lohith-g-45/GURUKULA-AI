
from typing import Dict, Any, List
from datetime import datetime
import json
from pathlib import Path
from app.services.data_loader import DataLoader
from app.orchestration.context_store import context_store
from app.database.user_store import user_profile_store
from app.utils.logger import logger


class InsightAgent:
    def __init__(self):
        self.data_loader = DataLoader()
        self.all_data = self.data_loader.load_all()
        self._load_insight_context()

    def _load_insight_context(self):
        try:
            context_path = Path(__file__).parent.parent.parent / "datasets" / "KAS" / "agent_contexts" / "insight_agent_context.json"
            if context_path.exists():
                with open(context_path, 'r', encoding='utf-8') as f:
                    self.insight_context = json.load(f)
            else:
                self.insight_context = {}
        except Exception as e:
            logger.error(f"Failed to load insight context: {e}")
            self.insight_context = {}

    def generate_insights(self, student_data: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            student_data = student_data or context_store.get("student_data", {})
            task_data = context_store.get("tasks", [])
            workflow_data = context_store.get("workflow_state", {})

            burnout_alerts = self._check_burnout(student_data, task_data)
            weak_subjects = self._identify_weak_subjects(student_data)
            performance_summary = self._generate_performance_summary(student_data, task_data)
            recommendations = self._generate_recommendations(student_data, burnout_alerts, weak_subjects)
            trends = self._extract_trends()

            insights = {
                "generated_at": datetime.now().isoformat(),
                "burnout_alerts": burnout_alerts,
                "weak_subjects": weak_subjects,
                "performance_summary": performance_summary,
                "recommendations": recommendations,
                "trends": trends
            }

            context_store.set("insights", insights)
            return insights
        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")
            return {
                "generated_at": datetime.now().isoformat(),
                "error": str(e)
            }

    def _check_burnout(self, student_data: Dict[str, Any], task_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        daily_hours = student_data.get("daily_study_hours", 0)
        consecutive_days = student_data.get("consecutive_study_days", 0)
        missed_tasks = len([t for t in task_data if t.get("status") == "missed"])

        if daily_hours > 10:
            alerts.append({
                "type": "excessive_hours",
                "severity": "high",
                "message": "Studying more than 10 hours daily may lead to burnout"
            })
        if consecutive_days > 7:
            alerts.append({
                "type": "no_rest_days",
                "severity": "medium",
                "message": "No rest days in the last week. Consider taking a break."
            })
        if missed_tasks > 3:
            alerts.append({
                "type": "task_overload",
                "severity": "medium",
                "message": "Multiple missed tasks, workload may be too high"
            })

        return alerts

    def _identify_weak_subjects(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        weak_subjects = []
        subject_scores = student_data.get("subject_scores", {})
        weightage_data = self.insight_context.get("data", {}).get("weightage", {}).get("subjects", {})

        for subject, score in subject_scores.items():
            if score < 60:
                weight_info = weightage_data.get(subject, {})
                weak_subjects.append({
                    "subject": subject,
                    "score": score,
                    "weightage": weight_info.get("prelims_weightage", 0),
                    "priority": weight_info.get("priority", "Medium"),
                    "recommendation": f"Focus on improving {subject} as it has {weight_info.get('prelims_weightage', 0)}% weightage"
                })

        # Add default weak subjects if no scores available
        if not weak_subjects:
            default_weak = ["Environment", "Ethics", "Disaster Management"]
            for subject in default_weak:
                weight_info = weightage_data.get(subject, {})
                if weight_info:
                    weak_subjects.append({
                        "subject": subject,
                        "score": 50,
                        "weightage": weight_info.get("prelims_weightage", 0),
                        "priority": weight_info.get("priority", "Medium"),
                        "recommendation": f"Consider reviewing {subject} fundamentals"
                    })

        return weak_subjects

    def _generate_performance_summary(self, student_data: Dict[str, Any], task_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_tasks = len(task_data)
        completed_tasks = len([t for t in task_data if t.get("status") == "completed"])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        summary = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": round(completion_rate, 2),
            "current_readiness": user_profile_store.get_readiness_score(),
            "study_streak": student_data.get("consecutive_study_days", 0),
            "last_updated": datetime.now().isoformat()
        }
        return summary

    def _generate_recommendations(self, student_data: Dict[str, Any], burnout_alerts: List[Dict[str, Any]], weak_subjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []

        # Add burnout-related recommendations
        for alert in burnout_alerts:
            if alert["type"] == "excessive_hours":
                recommendations.append({
                    "type": "schedule_adjustment",
                    "priority": "high",
                    "action": "Reduce daily study hours to 8-9 hours and include short breaks"
                })
            if alert["type"] == "no_rest_days":
                recommendations.append({
                    "type": "rest_day",
                    "priority": "high",
                    "action": "Schedule a rest day to avoid burnout"
                })

        # Add weak subject recommendations
        for weak in weak_subjects[:3]:
            recommendations.append({
                "type": "subject_focus",
                "priority": weak["priority"].lower(),
                "action": weak["recommendation"]
            })

        # Add general recommendations
        recommendations.append({
            "type": "revision",
            "priority": "medium",
            "action": "Include daily revision of key concepts"
        })
        recommendations.append({
            "type": "practice",
            "priority": "medium",
            "action": "Solve at least 50 MCQs daily"
        })

        return recommendations

    def _extract_trends(self) -> Dict[str, Any]:
        pyq_trends = self.insight_context.get("data", {}).get("pyq_trends", {})
        subject_priority = self.insight_context.get("data", {}).get("subject_priority", {})

        return {
            "high_frequency_topics": list(pyq_trends.get("topics", {}).keys())[:10],
            "high_priority_subjects": [s.get("name") for s in subject_priority.get("subjects", []) if s.get("priority") in ["High", "Very High"]]
        }


insight_agent = InsightAgent()

