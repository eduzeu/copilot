# Career Copilot

Career Copilot is a Next.js and FastAPI application for tracking job applications,
analyzing resumes with Gemini, and generating interview questions.

## Local setup

1. Copy `career-copilot-backend/.env.example` to `.env` and set `SECRET_KEY`.
2. From `career-copilot-backend`, create a virtual environment and run
   `pip install -r requirements.txt`.
3. Run `python create_tables.py`, then `uvicorn app.main:app --reload`.
4. Copy `career-copilot-frontend/.env.example` to `.env.local`.
5. From `career-copilot-frontend`, run `npm install` and `npm run dev`.

SQLite works by default. To use PostgreSQL, start `docker compose up -d db` and set
`DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/careercopilot`.
Supabase is optional; without its configuration, resume text is stored in the database
without uploading the original file. AI tools require `AI_KEY`.

## Verification

- Backend: `python -m pytest`
- Frontend: `npm run build`

Never commit `.env`, `.env.local`, virtual environments, or API credentials.
