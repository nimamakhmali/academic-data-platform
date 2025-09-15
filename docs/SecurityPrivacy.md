# Security, Privacy, and Compliance

## Authentication & Authorization
- OAuth2 Password + JWT (access/refresh)
- RBAC: Admin/Faculty/Student
- Password hashing (Argon2/bcrypt)

## Data Protection
- TLS in transit; at-rest encryption at DB/backup level (ops)
- PII minimization; access logging
- Rate limiting and input validation

## Privacy
- Anonymize datasets for analytics/research exports
- Retention policy for demo/test data

## Secure Coding & Operations
- Dependency scanning; secrets management via env vars
- Structured logs; audit trails for admin actions
