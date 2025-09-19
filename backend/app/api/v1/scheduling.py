from fastapi import APIRouter
from app.schemas.scheduling import ScheduleRequest, ScheduleResponse
from app.services.scheduling import greedy_schedule

router = APIRouter(prefix="/api/v1/scheduling", tags=["scheduling"])


@router.post("/generate", response_model=ScheduleResponse)
def generate_schedule(payload: ScheduleRequest):
	return greedy_schedule(payload)
