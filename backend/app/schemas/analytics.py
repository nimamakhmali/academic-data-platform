from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class StudentFeatures(BaseModel):
    student_id: int
    gpa: float = Field(ge=0.0, le=4.0)
    attendance_rate: float = Field(ge=0.0, le=1.0)
    credit_hours: int = Field(ge=0)
    failed_courses: int = Field(ge=0)
    age: Optional[int] = Field(None, ge=16, le=100)
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")


class AtRiskPrediction(BaseModel):
    student_id: int
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: str = Field(regex="^(low|medium|high)$")
    confidence: float = Field(ge=0.0, le=1.0)
    factors: List[str] = Field(default_factory=list)


class AnalyticsRequest(BaseModel):
    students: List[StudentFeatures]
    model_version: str = "v1"


class AnalyticsResponse(BaseModel):
    predictions: List[AtRiskPrediction]
    model_info: dict
    generated_at: datetime
