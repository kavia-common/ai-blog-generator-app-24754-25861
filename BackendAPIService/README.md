# BackendAPIService

FastAPI backend for the AI Blog Generator App.

## Features
- JWT authentication (register/login)
- PostgreSQL via SQLAlchemy
- Blog posts CRUD with versioning
- AI-powered generation using OpenAI-compatible API (httpx)
- Exports: HTML and Markdown server-side, PDF placeholder
- Admin stats
- CORS and basic error handling
- OpenAPI schema at `/docs` and `/interfaces/openapi.json` via utility

## Environment Variables
Copy `.env.example` to `.env` and set values as needed.

Required:
- DATABASE_URL (e.g., `postgresql://appuser:dbuser123@localhost:5000/ai_blog_generator_db`)
- JWT_SECRET (set a strong secret)
- CORS_ORIGINS (default: `http://localhost:3000` for the React app)

Optional:
- BACKEND_PORT (default: 8000)
- AI_PROVIDER (default: `openai-compatible`)
- AI_API_KEY (if empty, placeholder generation is used)
- AI_MODEL (default: `gpt-4o-mini`)
- OPENAI_BASE_URL (defaults to `https://api.openai.com/v1`)
- PDF_ENGINE (set to `none` to disable, placeholder behavior)

## Quick Start (Local)
1) Database
   - Ensure PostgreSQL is running and accessible.
   - Confirm DB name and port:
     - DB name: `ai_blog_generator_db`
     - Port: `5000`
   - Example connection string (matches `.env.example`):
     ```
     postgresql://appuser:dbuser123@localhost:5000/ai_blog_generator_db
     ```
   - Create the database and user if not existing.

2) Backend
   - Create `.env` from `.env.example` and adjust values.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the service:
     ```
     uvicorn src.api.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}
     ```
   - Docs: http://localhost:8000/docs

3) Frontend
   - Ensure the frontend `.env` has:
     - `REACT_APP_API_BASE=http://localhost:8000`
   - Start the frontend (see FrontendWebApplication README).

On first backend start, database tables are created automatically.

## CORS
CORS is configured via `CORS_ORIGINS` env var. For local dev, set:
```
CORS_ORIGINS=http://localhost:3000
```

## Smoke Test (End-to-End)
From the running app (frontend at http://localhost:3000, backend at http://localhost:8000):

1. Register a new user:
   - POST /auth/register (via frontend UI signup)
2. Login:
   - Obtain JWT via /auth/login (handled by UI)
3. Generate content:
   - Use the "Generate" feature; with no AI_API_KEY the app returns placeholder content deterministically.
4. Save post:
   - Save generated content; verify it appears in "My Posts".
5. Update post:
   - Edit and save; verify a new version is created.
6. Export:
   - Export to Markdown (/exports/{id}/markdown) and HTML (/exports/{id}/html) via UI.
   - PDF export returns a placeholder note when `PDF_ENGINE=none`.
7. Confirm admin stats (optional):
   - If you have an admin user, check `/admin/stats`.

## Regenerate OpenAPI spec
```
python -m src.api.generate_openapi
```
