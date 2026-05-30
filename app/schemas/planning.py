
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class PlanningRequest(BaseModel):
    exam: str = "KAS"
    readiness_score: Optional[float] = 70.0
    available_hours_per_day: Optional[float] = 6.0
    exam_date_distance_days: Optional[int] = 180
    weak_subjects: Optional[List[str]] = []
    refresh: bool = False


class PlanningResponse(BaseModel):
    model_config = {"extra": "allow"}
    success: bool
    data: Any
    usage: Dict[str, int] = {}
    cached: bool = False
