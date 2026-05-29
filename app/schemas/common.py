
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class StandardResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None


class UserProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    exam: Optional[str] = "KAS"
    readiness_score: Optional[float] = 70.0
    available_hours_per_day: Optional[float] = 6.0
    weak_subjects: Optional[List[str]] = []
    study_goals: Optional[List[str]] = []


class UserProfileResponse(StandardResponse):
    data: Optional[Dict[str, Any]] = None


class StudentAnalysisRequest(BaseModel):
    student_data: Optional[Dict[str, Any]] = None
    recent_tasks: Optional[List[Dict[str, Any]]] = []
    mock_scores: Optional[List[Dict[str, Any]]] = []


class StudentAnalysisResponse(StandardResponse):
    data: Optional[Dict[str, Any]] = None


class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    readiness_score: float
    study_hours_today: float
    upcoming_tasks: int
    recent_activities: List[Dict[str, Any]]


class DashboardResponse(StandardResponse):
    data: Optional[DashboardStats] = None


class AgentStatus(BaseModel):
    name: str
    status: str  # "active", "idle", "error"
    last_run: Optional[str] = None
    success_rate: float


class AgentsStatusResponse(StandardResponse):
    data: Optional[List[AgentStatus]] = None

