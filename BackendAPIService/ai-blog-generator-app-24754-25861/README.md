# AI Blog Generator - Backend Workspace

This workspace contains the BackendAPIService for the AI Blog Generator app.

See:
- BackendAPIService/README.md for backend setup and smoke tests.
- Ensure the FrontendWebApplication container has `.env` with:
  - `REACT_APP_API_BASE=http://localhost:8000`

Multi-container Quick Start:
1) Start Database (PostgreSQL)
   - Ensure DB `ai_blog_generator_db` is running on port 5000 with user `appuser` / password `dbuser123`.
2) Start Backend
   - In `BackendAPIService`, copy `.env.example` to `.env`, adjust values, and run:
     `uvicorn src.api.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}`
3) Start Frontend
   - In FrontendWebApplication, ensure `.env` includes:
     `REACT_APP_API_BASE=http://localhost:8000`
   - Start the dev server on port 3000.

Then follow the Smoke Test steps in BackendAPIService/README.md.
