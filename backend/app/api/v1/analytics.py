from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse
from app.services.analytics import analyze_at_risk_students
from app.services.authz import require_roles

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.post("/at-risk", response_model=AnalyticsResponse)
def analyze_students_at_risk(
    request: AnalyticsRequest,
    current_user = Depends(require_roles("faculty", "admin"))
):
    """
    Analyze students to identify those at risk of academic failure.
    Requires faculty or admin role.
    """
    try:
        return analyze_at_risk_students(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/health")
def analytics_health():
    """Health check for analytics service"""
    return {"status": "ok", "service": "analytics"}
