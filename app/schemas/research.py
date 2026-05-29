from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class FrequentTopic(BaseModel):
    topic: str
    frequency: int


class ResearchSummary(BaseModel):
    exam_overview: str
    high_priority_subjects: List[str]
    frequent_topics: List[FrequentTopic]


class Metadata(BaseModel):
    conducted_by: str
    stages: List[str]
    qualification: str
    difficulty: str
    preparation_duration: Optional[str] = None
    exam_type: Optional[str] = None


class ResearchData(BaseModel):
    research_summary: ResearchSummary
    metadata: Metadata
    actionable_insights: List[str]


class ResearchRequest(BaseModel):
    exam: str = "KAS"


class ResearchResponse(BaseModel):
    success: bool
    data: ResearchData
    usage: Dict[str, int]
