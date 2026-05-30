
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ResearchRequest(BaseModel):
    exam: str = "KAS"
    refresh: bool = False


class ResearchResponse(BaseModel):
    success: bool
    data: Any
    usage: Dict[str, int] = {}
    cached: bool = False


class StudentAnalysisRequest(BaseModel):
    student_data: Optional[Dict[str, Any]] = None
    refresh: bool = False


class StudentAnalysisResponse(BaseModel):
    success: bool
    data: Any
    usage: Dict[str, int] = {}
    cached: bool = False
