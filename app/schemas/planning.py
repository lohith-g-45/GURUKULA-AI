
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Topic(BaseModel):
    model_config = {"extra": "allow"}
    name: str
    hours: float
    priority: str


class SubjectPlan(BaseModel):
    model_config = {"extra": "allow"}
    subject: str
    priority: str
    allocated_hours: float
    topics: List[Topic]


class Stage(BaseModel):
    model_config = {"extra": "allow"}
    stage_name: str
    duration_weeks: int
    focus_subjects: List[str]
    weekly_hours: float
    objectives: Optional[str] = None


class PreparationRoadmap(BaseModel):
    model_config = {"extra": "allow"}
    duration_months: int
    stages: List[Stage]


class WeeklySchedule(BaseModel):
    model_config = {"extra": "allow"}
    daily_targets: List[str]
    mock_test_frequency: str
    study_days_per_week: Optional[int] = 6
    daily_hours: Optional[float] = 6.0


class DailyScheduleItem(BaseModel):
    model_config = {"extra": "allow"}
    time_slot: str
    subject: str
    activity: str


class DailySchedule(BaseModel):
    model_config = {"extra": "allow"}
    day: str
    items: List[DailyScheduleItem]


class Milestone(BaseModel):
    model_config = {"extra": "allow"}
    type: str
    description: str
    criteria: List[str]
    reward: Optional[str] = None


class RevisionCycle(BaseModel):
    model_config = {"extra": "allow"}
    subject: str
    priority_score: float
    revision_frequency: str
    revision_days: List[int]


class MockSchedule(BaseModel):
    model_config = {"extra": "allow"}
    mock_type: str
    frequency: str
    focus_subjects: List[str]
    post_mock_analysis: bool


class PlanningData(BaseModel):
    model_config = {"extra": "allow"}
    preparation_roadmap: PreparationRoadmap
    subject_plan: List[SubjectPlan]
    weekly_schedule: WeeklySchedule
    daily_schedule: Optional[List[Dict[str, Any]]] = []
    milestones: Optional[List[Dict[str, Any]]] = []
    revision_cycles: Optional[List[Dict[str, Any]]] = []
    mock_schedule: Optional[Dict[str, Any]] = None


class PlanningRequest(BaseModel):
    exam: str = "KAS"
    readiness_score: Optional[float] = 70.0
    available_hours_per_day: Optional[float] = 6.0
    exam_date_distance_days: Optional[int] = 180
    weak_subjects: Optional[List[str]] = []


class PlanningResponse(BaseModel):
    model_config = {"extra": "allow"}
    success: bool
    data: PlanningData
    usage: Dict[str, int]

