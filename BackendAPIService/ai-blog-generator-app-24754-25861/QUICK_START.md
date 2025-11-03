# Quick Start (Multi-Container)

Order:
1) Database
2) Backend
3) Frontend

Database (PostgreSQL):
- Ensure the following connection is valid:
  postgresql://appuser:dbuser123@localhost:5000/ai_blog_generator_db

Backend:
- Location: BackendAPIService
- Copy `.env.example` to `.env` and update:
  - DATABASE_URL=postgresql://appuser:dbuser123@localhost:5000/ai_blog_generator_db
  - JWT_SECRET=your_jwt_secret_here
  - CORS_ORIGINS=http://localhost:3000
  - BACKEND_PORT=8000
  - AI_PROVIDER=openai-compatible
  - AI_API_KEY= (optional)
  - AI_MODEL=gpt-4o-mini
  - PDF_ENGINE=none
- Start:
  uvicorn src.api.main:app --host 0.0.0.0 --port 8000

Frontend:
- Ensure `.env` contains:
  REACT_APP_API_BASE=http://localhost:8000
- Start dev server (port 3000 by default)

Run Smoke Tests:
- See SMOKE_TESTS.md
