# Data Model (ERD) and Data Dictionary

## Entities
- User(id, email, password_hash, role)
- Student(id, user_id, student_no, entry_year)
- Faculty(id, user_id, department, rank)
- Course(id, code, title, credits, department)
- Enrollment(id, student_id, course_id, term, grade)
- ResearchItem(id, title, type, year, owner_faculty_id)

## Relationships
- User 1—1 Student
- User 1—1 Faculty
- Student N—M Course via Enrollment
- Faculty 1—N ResearchItem

## Indexing & Constraints
- Unique: User.email, Student.student_no, Course.code
- FKs: Student.user_id → User.id، Enrollment.student_id/course_id → Student/Course

## Data Dictionary (excerpt)
- grade: NUMERIC(3,1) nullable
- term: VARCHAR(10) (e.g., 1402-1)
