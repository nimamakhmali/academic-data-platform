import pytest
from httpx import AsyncClient
from app.main import app
from app.schemas.analytics import StudentFeatures


@pytest.mark.asyncio
async def test_analytics_at_risk_prediction():
    """Test at-risk student prediction endpoint"""
    # Create test data
    test_students = [
        StudentFeatures(
            student_id=1,
            gpa=1.8,
            attendance_rate=0.5,
            credit_hours=9,
            failed_courses=3,
            age=20,
            gender="male"
        ),
        StudentFeatures(
            student_id=2,
            gpa=3.5,
            attendance_rate=0.95,
            credit_hours=15,
            failed_courses=0,
            age=21,
            gender="female"
        ),
        StudentFeatures(
            student_id=3,
            gpa=2.3,
            attendance_rate=0.7,
            credit_hours=12,
            failed_courses=1,
            age=22,
            gender="other"
        )
    ]
    
    payload = {
        "students": [student.dict() for student in test_students],
        "model_version": "v1"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First register a faculty user for authentication
        faculty_data = {
            "email": "faculty@test.com",
            "username": "faculty_user",
            "password": "testpass123",
            "role": "faculty"
        }
        await ac.post("/api/v1/auth/register", json=faculty_data)
        
        # Login to get token
        login_data = {
            "username": "faculty@test.com",
            "password": "testpass123"
        }
        login_resp = await ac.post("/api/v1/auth/login", data=login_data)
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test analytics endpoint
        resp = await ac.post("/api/v1/analytics/at-risk", json=payload, headers=headers)
        assert resp.status_code == 200
        
        data = resp.json()
        assert "predictions" in data
        assert "model_info" in data
        assert "generated_at" in data
        assert len(data["predictions"]) == 3
        
        # Check prediction structure
        for prediction in data["predictions"]:
            assert "student_id" in prediction
            assert "risk_score" in prediction
            assert "risk_level" in prediction
            assert "confidence" in prediction
            assert "factors" in prediction
            assert 0 <= prediction["risk_score"] <= 1
            assert prediction["risk_level"] in ["low", "medium", "high"]
            assert 0 <= prediction["confidence"] <= 1


@pytest.mark.asyncio
async def test_analytics_unauthorized_access():
    """Test that analytics endpoint requires authentication"""
    payload = {
        "students": [],
        "model_version": "v1"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/analytics/at-risk", json=payload)
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_analytics_student_role_denied():
    """Test that students cannot access analytics"""
    # Register and login as student
    student_data = {
        "email": "student@test.com",
        "username": "student_user",
        "password": "testpass123",
        "role": "student"
    }
    await ac.post("/api/v1/auth/register", json=student_data)
    
    login_data = {
        "username": "student@test.com",
        "password": "testpass123"
    }
    login_resp = await ac.post("/api/v1/auth/login", data=login_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "students": [],
        "model_version": "v1"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/analytics/at-risk", json=payload, headers=headers)
        assert resp.status_code == 403


@pytest.mark.asyncio
async def test_analytics_health_check():
    """Test analytics health endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/analytics/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "analytics"
