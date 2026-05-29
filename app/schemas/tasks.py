
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    topic: Optional[str] = None
    priority: str = "Medium"
    estimated_hours: float
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = []


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    priority: Optional[str] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    completed_at: Optional[datetime] = None


class Task(TaskBase):
    id: str
    status: str = "pending"
    progress: float = 0.0
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    success: bool
    data: List[Task]
    count: int


class TaskResponse(BaseModel):
    success: bool
    data: Task


class RevisionRequest(BaseModel):
    subject: Optional[str] = None
    recent_tasks: Optional[List[str]] = []
    current_readiness: Optional[float] = 70.0


class RevisionResponse(BaseModel):
    success: bool
    data: Dict[str, Any]


class ReplanningRequest(BaseModel):
    current_tasks: Optional[List[Task]] = []
    missed_tasks: Optional[List[str]] = []
    new_availability: Optional[float] = None
    readiness_change: Optional[float] = None


class ReplanningResponse(BaseModel):
    success: bool
    data: Dict[str, Any]


class InsightRequest(BaseModel):
    student_data: Optional[Dict[str, Any]] = None


class InsightResponse(BaseModel):
    success: bool
    data: Dict[str, Any]


class WorkflowStatusResponse(BaseModel):
    success: bool
    data: Dict[str, Any]


class WorkflowRunRequest(BaseModel):
    context: Optional[Dict[str, Any]] = None
