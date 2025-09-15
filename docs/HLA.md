# High-Level Architecture (HLA)

## لایه‌ها
- Presentation: React + Tailwind (FA/EN), Router, Query, Charts
- API/Service: FastAPI (Python), REST + WebSocket
- AI/Analytics: Python pipelines (scikit-learn → PyTorch)
- Data: PostgreSQL (OLTP), Redis (Cache/Queue), (MongoDB optional)
- Infra: Docker, GitHub Actions CI, Cloud VM/K8s (بعدی)

## اجزا و مسئولیت‌ها
- API Gateway/Backend: احراز هویت، مجوز، اعتبارسنجی، منطق دامنه
- Analytics Service: آموزش/استنباط مدل‌ها، ذخیره آرتیفکت‌ها
- Reporting: تولید PDF/CSV
- Frontend App: UI داشبوردها، فرم‌ها، فیلترها

## جریان داده (نمونه)
1. ورود کاربر → دریافت JWT
2. فراخوانی CRUD → Postgres
3. درخواست پیش‌بینی → سرویس Analytics → نتیجه و متادیتا
4. تولید گزارش → فایل خروجی قابل دانلود

## پترن‌ها
- 3-tier، Twelve-Factor، Clean Architecture در backend
- RBAC، Logging ساختاریافته، Health endpoints
