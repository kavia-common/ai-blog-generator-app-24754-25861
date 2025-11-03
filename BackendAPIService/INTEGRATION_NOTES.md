# Integration Notes

- FrontendWebApplication/.env.example should include:
  REACT_APP_API_BASE=http://localhost:8000

- BackendAPIService/.env.example includes:
  DATABASE_URL=postgresql://appuser:dbuser123@localhost:5000/ai_blog_generator_db
  JWT_SECRET=your_jwt_secret_here
  CORS_ORIGINS=http://localhost:3000
  AI_PROVIDER / AI_API_KEY / AI_MODEL
  BACKEND_PORT=8000
  PDF_ENGINE=none

- Database container should expose Postgres on port 5000 with DB name `ai_blog_generator_db`.

- Start order: Database -> Backend -> Frontend.

- Smoke testing steps are in SMOKE_TESTS.md.
