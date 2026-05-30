
from fastapi import APIRouter
from datetime import datetime, timedelta
from app.schemas.common import DashboardResponse, DashboardStats
from app.database.task_store import task_store
from app.database.user_store import user_profile_store, study_session_store, mock_score_store
from app.utils.logger import logger


router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


def get_recent_activities() -> list[dict]:
    tasks = task_store.get_all_tasks()
    recent = []
    
    # Recent completed tasks
    completed_recent = [t for t in tasks if t.status == "completed" and hasattr(t, "updated_at")][-5:]
    for task in completed_recent:
        recent.append({
            "activity": "Task completed",
            "subject": task.subject,
            "title": task.title,
            "time": "Recently"
        })
    
    # Recent mock scores
    mock_scores = mock_score_store.get_all_scores()[-3:]
    for score in mock_scores:
        recent.append({
            "activity": "Mock test taken",
            "subject": score.get('subject', 'General'),
            "score": score.get('score', 0),
            "time": score.get('taken_at', 'Recently')
        })
    
    return recent[-10:]


@router.get("", response_model=DashboardResponse)
async def get_dashboard_stats():
    logger.info("Fetching dashboard stats")
    tasks = task_store.get_all_tasks()
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == "completed"])
    pending_tasks = len([t for t in tasks if t.status == "pending"])
    
    upcoming_tasks = len([t for t in tasks if t.status == "pending" and hasattr(t, "due_date")])
    
    recent_activities = get_recent_activities()
    
    readiness_score = user_profile_store.get_readiness_score()
    study_hours_today = study_session_store.get_total_hours_today()
    
    stats = DashboardStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        readiness_score=readiness_score,
        study_hours_today=study_hours_today,
        upcoming_tasks=upcoming_tasks,
        recent_activities=recent_activities
    )
    
    return DashboardResponse(
        success=True,
        data=stats
    )

