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

## Setup
1. Create and configure the `.env` file based on `.env.example`.
2. Install dependencies:
   pip install -r requirements.txt
3. Run the service:
   uvicorn src.api.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}

On first start, database tables will be created automatically.

To regenerate OpenAPI spec:
   python -m src.api.generate_openapi
