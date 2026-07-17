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

Career Coach includes a per-user online UCB1 learning policy. Rating a response
updates the preferred coaching strategy for that mode, allowing future responses
to favor approaches that have been helpful for that user. Run `python create_tables.py`
after pulling schema changes to create the learning tables.

## Verification

- Backend: `python -m pytest`
- Frontend: `npm run build`

## Datadog backend monitoring

Career Copilot supports Datadog APM for FastAPI request traces, SQLAlchemy database
queries, error tracking, and Python runtime metrics. The Datadog API key is only used
by the local Agent and must never be committed.

1. Create a Datadog API key in your Datadog organization.
2. Install the updated backend dependencies:

   ```powershell
   cd career-copilot-backend
   python -m pip install -r requirements.txt
   ```

3. From the repository root, start the optional Datadog Agent:

   ```powershell
   $env:DD_API_KEY="your-datadog-api-key"
   $env:DD_SITE="datadoghq.com"
   docker compose --profile observability up -d datadog-agent
   ```

   Change `DD_SITE` if the Datadog organization uses another site, such as
   `us3.datadoghq.com` or `datadoghq.eu`.

4. Start the backend through Datadog's automatic instrumentation:

   ```powershell
   cd career-copilot-backend
   $env:DD_SERVICE="career-copilot-backend"
   $env:DD_ENV="development"
   $env:DD_VERSION="0.1.0"
   $env:DD_AGENT_HOST="127.0.0.1"
   $env:DD_TRACE_AGENT_PORT="8126"
   $env:DD_RUNTIME_METRICS_ENABLED="true"
   $env:DD_LOGS_INJECTION="true"
   ddtrace-run python -m uvicorn app.main:app --reload
   ```

5. Exercise endpoints such as `/health`, then open **APM > Services** in Datadog and
   select `career-copilot-backend`. To inspect the local Agent, run
   `docker compose logs datadog-agent`.

To run the backend without Datadog, continue using the normal `uvicorn` command.

Never commit `.env`, `.env.local`, virtual environments, or API credentials.
