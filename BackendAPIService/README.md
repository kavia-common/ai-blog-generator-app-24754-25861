# AI Blog Generator - Backend API Service (FastAPI)

Overview
- Exposes RESTful endpoints for auth, content generation, posts management, admin, and exports.
- Serves on http://localhost:8000 in local development.

Required Environment Variables (example)
- API_PORT=8000
- CORS_ALLOWED_ORIGINS=http://localhost:3000
- DB_HOST=localhost
- DB_PORT=5000
- DB_NAME=ai_blog_generator_db
- DB_USER=postgres
- DB_PASSWORD=postgres
- JWT_SECRET=please_change_me
- JWT_ALG=HS256

CORS
- Ensure `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000` so the React frontend can call the API.

Database
- Connects to PostgreSQL `ai_blog_generator_db` on port `5000`.
- See the Database container README for details.

Quick Start
1) Start Database (port 5000, DB ai_blog_generator_db)
2) Start Backend (port 8000; set CORS_ALLOWED_ORIGINS to http://localhost:3000)
3) Start Frontend (REACT_APP_API_BASE=http://localhost:8000)

OpenAPI
- See `interfaces/openapi.json` for current API description (health, websocket-info placeholders).
