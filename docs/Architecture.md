# System Architecture

## Component View
- Web App (React)
- API Service (FastAPI)
- Analytics Module (Python/ML)
- Database (PostgreSQL)
- Cache/Queue (Redis)
- Observability (logs/metrics)

## Runtime View
- REST over HTTPS; JSON payloads; JWT Bearer
- WebSocket for live notifications (optional MVP)

## Deployment View
- Dev: Docker Compose (web, api, db, redis)
- Prod: Docker on VM; K8s later

## Data Flows
- ETL-lite: CSV import → validate → persist → aggregate KPIs

## Quality Attributes
- Security, Scalability, Reliability, Observability, i18n
