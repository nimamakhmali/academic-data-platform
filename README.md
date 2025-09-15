# Academic Data Management & AI Analysis Platform

An enterprise-grade platform for managing and analyzing academic data (students, faculty, courses, enrollments, research) with ML-driven insights, dashboards, and open APIs.

## Highlights
- React frontend, FastAPI backend, PostgreSQL + Redis, ML analytics
- OAuth2/JWT, RBAC, dashboards, reporting, OpenAPI contract
- Dockerized dev with CI/CD guidance; scalable deployment path

## Documentation
See `docs/` for RFP, SRS, HLA, Architecture, ERD, OpenAPI, Test Plan, Security/Privacy, DevOps, and Roadmap.

## Quickstart (Backend)

- Local (Python):
  - Create venv, install `backend/requirements.txt`
  - Run: `python -m app` from `backend/`
- Docker Compose:
  - `docker compose up --build`
  - API: `http://localhost:8000/health`
