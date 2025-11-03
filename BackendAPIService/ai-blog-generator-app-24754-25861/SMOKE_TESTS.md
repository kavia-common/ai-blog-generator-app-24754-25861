# Smoke Tests - AI Blog Generator (Local Dev)

Prereqs:
- Database running: PostgreSQL at port 5000 with DB `ai_blog_generator_db`
- Backend running at http://localhost:8000 with `.env` configured
- Frontend running at http://localhost:3000 with `REACT_APP_API_BASE=http://localhost:8000`

Steps:
1) Registration
   - In the frontend, navigate to Sign Up.
   - Register a new user with email and password.
   - Expect 200 OK and user record created.

2) Login
   - Login with the created user.
   - Expect JWT stored in client (UI should indicate logged-in state).

3) Generate Content
   - Go to Generate screen.
   - Enter a topic (e.g., "Retro computing in modern web development") and optional style.
   - If AI_API_KEY is unset, verify placeholder content displays deterministically.

4) Save Post
   - Save generated content.
   - Navigate to "My Posts" and confirm the post is present with version = 1.

5) Edit and Versioning
   - Open the post, make an edit, and save.
   - Verify version increments to 2.
   - Check version history shows two entries.

6) Export
   - Export as Markdown and HTML.
   - Verify download or preview contains expected content.
   - Export as PDF: expect a placeholder note when PDF_ENGINE=none.

7) Admin Stats (optional)
   - If logged in as admin, check Admin Stats to see counts for users, posts, versions, and exports.

Troubleshooting:
- CORS errors: ensure backend `.env` has `CORS_ORIGINS=http://localhost:3000` and restart backend.
- API base mismatch: ensure frontend `.env` has `REACT_APP_API_BASE=http://localhost:8000`.
- DB errors: confirm `DATABASE_URL` matches a reachable Postgres instance and the DB exists.
