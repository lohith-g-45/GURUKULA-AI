
from fastapi import APIRouter
from app.schemas.common import DashboardResponse, DashboardStats
from app.database.task_store import task_store
from app.utils.logger import logger


router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@router.get("", response_model=DashboardResponse)
async def get_dashboard_stats():
    logger.info("Fetching dashboard stats")
    tasks = task_store.get_all_tasks()
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == "completed"])
    pending_tasks = len([t for t in tasks if t.status == "pending"])
    
    recent_activities = [
        {"activity": "Task completed", "subject": "Polity", "time": "2 hours ago"},
        {"activity": "Mock test taken", "subject": "History", "time": "5 hours ago"},
        {"activity": "Study session started", "subject": "Geography", "time": "1 day ago"}
    ]
    
    stats = DashboardStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        readiness_score=72.5,
        study_hours_today=4.5,
        upcoming_tasks=5,
        recent_activities=recent_activities
    )
    
    return DashboardResponse(
        success=True,
        data=stats
    )

