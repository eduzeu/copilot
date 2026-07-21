# Career Copilot

Career Copilot is a full-stack job-search platform that combines application tracking,
résumé analysis, interview preparation, and a personalized AI career coach. The coach
uses each user's career profile, latest résumé, application pipeline, completed actions,
and feedback to provide practical next steps instead of generic career advice.

## Core features

- Secure account registration, login, session cookies, and logout
- Career profiles for students, recent graduates, and professionals
- Application tracking with dashboard metrics and pipeline statuses
- PDF and DOCX résumé upload and text extraction
- General résumé feedback and résumé-to-job matching
- AI-generated technical, behavioral, and system-design questions
- Personalized career coaching for weekly planning, applications, interviews, and skill gaps
- Trackable weekly actions with completion status and recorded outcomes
- Feedback-driven coaching strategy selection using a per-user UCB1 policy
- AI response validation, caching, quotas, provider timeouts, and deterministic fallbacks
- PostgreSQL migrations, Docker deployment, CI, readiness checks, and optional Datadog APM

## Technology stack

| Layer | Technologies |
| --- | --- |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.11, Pydantic, SQLAlchemy |
| Database | PostgreSQL 16; SQLite is supported for tests and simple local use |
| AI | Google Gemini through `google-genai` |
| Storage | Supabase Storage is optional; extracted text remains in PostgreSQL |
| Observability | Datadog APM through `ddtrace` |
| Infrastructure | Docker Compose, Alembic, GitHub Actions |

## Architecture

```mermaid
flowchart LR
    U["User"] --> F["Next.js frontend"]
    F -->|"HTTP-only session cookie + JSON"| B["FastAPI backend"]
    B --> P[("PostgreSQL")]
    B --> G["Gemini API"]
    B -. optional files .-> S["Supabase Storage"]
    B -. traces and metrics .-> D["Datadog Agent"]
    P --> C["Profile, applications, résumés, actions, AI cache, feedback"]
```

The backend is the security and orchestration boundary. The frontend never calls Gemini
directly and never receives the Gemini API key.

## Repository structure

```text
career/
├── career-copilot-backend/
│   ├── alembic/                 Database migrations
│   ├── app/
│   │   ├── api/routes/          FastAPI endpoints
│   │   ├── core/                Settings and authentication
│   │   ├── db/                  SQLAlchemy engine and sessions
│   │   ├── models/              Database models
│   │   ├── schemas/             Request and response validation
│   │   ├── services/            Business logic, AI, caching, and learning
│   │   └── utils/               Extraction and prompt helpers
│   ├── evals/                   AI evaluation rubric
│   └── tests/                   Backend regression tests
├── career-copilot-frontend/
│   ├── app/                     Next.js App Router pages
│   ├── components/              Shared UI components
│   └── lib/                     API, authentication, and shared types
├── .github/workflows/ci.yml     Continuous integration
└── docker-compose.yml           Local full-stack orchestration
```

## Prerequisites

- Python 3.11
- Node.js 20 or newer
- Docker Desktop for PostgreSQL and full-stack containers
- A Gemini API key for live AI features

Supabase and Datadog are optional.

## Quick start with Docker

From the repository root:

```powershell
$env:SECRET_KEY="replace-with-a-random-secret-at-least-32-characters"
$env:AI_KEY="your-gemini-api-key"
docker compose up --build db backend frontend
```

Open:

- Frontend: `http://127.0.0.1:3000`
- Backend documentation: `http://127.0.0.1:8000/docs`
- Backend readiness: `http://127.0.0.1:8000/health/ready`

Stop the stack with:

```powershell
docker compose down
```

Database data is preserved in the `pgdata` Docker volume. Do not add `-v` unless you
intend to delete the local database.

## Manual local setup

### 1. Start PostgreSQL

```powershell
docker compose up -d db
```

### 2. Configure and start the backend

```powershell
cd career-copilot-backend
Copy-Item .env.example .env
```

Update `.env` with at least:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/careercopilot
SECRET_KEY=replace-with-a-random-secret-at-least-32-characters
AI_KEY=your-gemini-api-key
```

Create and activate the environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Apply migrations and start FastAPI:

```powershell
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

Use `python -m uvicorn` to guarantee that Uvicorn runs from the activated environment.

### 3. Configure and start the frontend

In another terminal:

```powershell
cd career-copilot-frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

The default frontend configuration points to `http://127.0.0.1:8000`.

## Environment variables

### Backend

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `DATABASE_URL` | Production | SQLite | SQLAlchemy database connection |
| `SECRET_KEY` | Yes | Development placeholder | Signs authentication tokens; production requires 32+ characters |
| `ENV` | No | `dev` | Use `production` or `prod` to enable production validation |
| `DEBUG` | No | `false` | Must remain false in production |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Session/token lifetime |
| `DATABASE_CONNECT_TIMEOUT_SECONDS` | No | `5` | Bounds unavailable database connections |
| `AI_KEY` | AI features | Empty | Gemini API key |
| `AI_MODEL` | No | `gemini-2.5-flash` | Gemini model used by the backend |
| `AI_TIMEOUT_SECONDS` | No | `30` | Maximum provider request time |
| `AI_DAILY_REQUESTS_PER_USER` | No | `30` | Per-user daily AI budget |
| `AI_CACHE_TTL_SECONDS` | No | `86400` | Analysis cache lifetime |
| `PROMPT_VERSION` | No | Date-based version | Invalidates caches after intentional prompt changes |
| `CORS_ORIGINS` | Yes when deployed | Local frontend origins | Comma-separated allowed frontend origins |
| `MAX_UPLOAD_BYTES` | No | `10485760` | Maximum résumé upload size |
| `SUPABASE_URL` | Optional | Empty | Supabase project URL |
| `SUPABASE_KEY` | Optional | Empty | Supabase API key |
| `SUPABASE_BUCKET` | Optional | `resumes` | Résumé storage bucket |

Never expose `AI_KEY`, `SECRET_KEY`, Supabase secrets, or Datadog API keys through a
`NEXT_PUBLIC_` variable.

### Frontend

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | Yes when deployed | `http://127.0.0.1:8000` | Public FastAPI base URL |

## API overview

Interactive OpenAPI documentation is available at `/docs` while the backend is running.
Protected routes accept the HTTP-only `career_copilot_session` cookie. Bearer tokens are
also supported for API clients and tests.

### Health

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/health` | Backward-compatible liveness response |
| `GET` | `/health/live` | Confirms the backend process is running |
| `GET` | `/health/ready` | Verifies that the backend can query the database |

### Authentication and users

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Creates an account |
| `POST` | `/auth/login` | Verifies credentials and sets the session cookie |
| `POST` | `/auth/logout` | Clears the session cookie |
| `GET` | `/users/me` | Returns the current user |
| `PUT` | `/users/me` | Updates the current user |
| `DELETE` | `/users/me` | Deletes the current user |

Login failures are throttled per IP and email combination.

### Career profile and dashboard

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/profile/` | Returns or initializes the career profile |
| `PUT` | `/profile/` | Updates the profile and recalculates completeness |
| `GET` | `/dashboard/` | Returns application pipeline metrics |

### Applications

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/applications/` | Lists the current user's applications |
| `POST` | `/applications/` | Creates an application |
| `GET` | `/applications/{application_id}` | Returns one owned application |
| `PUT` | `/applications/{application_id}` | Updates one owned application |
| `DELETE` | `/applications/{application_id}` | Deletes one owned application |

### Résumés and AI analysis

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/resumes/` | Lists uploaded résumés |
| `POST` | `/resumes/upload` | Extracts and stores a PDF or DOCX résumé |
| `GET` | `/resumes/{resume_id}` | Returns one owned résumé |
| `PUT` | `/resumes/{resume_id}` | Updates résumé metadata |
| `DELETE` | `/resumes/{resume_id}` | Deletes one owned résumé |
| `POST` | `/analysis/resume-feedback` | Produces general résumé feedback |
| `POST` | `/analysis/job-match` | Compares an uploaded résumé with a job description |
| `POST` | `/analysis/score` | Compares provided résumé text with a job description |
| `POST` | `/analysis/bullet/general` | Reviews one résumé bullet |
| `POST` | `/analysis/bullet/llm` | Reviews a bullet against a job description |

Non-résumé documents return `is_resume: false` and a `null` score. They are never shown
as a zero-quality résumé.

### Career coach

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/coach/chat` | Produces personalized conversational advice |
| `POST` | `/coach/questions` | Generates interview questions |
| `PUT` | `/coach/interactions/{interaction_id}/feedback` | Records helpful/not-helpful feedback |
| `GET` | `/coach/actions` | Lists trackable plan actions |
| `POST` | `/coach/actions` | Creates a custom action |
| `PUT` | `/coach/actions/{action_id}` | Updates status or records an outcome |

## How the AI layer works

Career Copilot does not train or host a foundation model. It orchestrates Gemini using
grounded application data and deterministic safeguards:

1. The authenticated user's profile, recent applications, latest résumé, conversation,
   and action outcomes are selected from PostgreSQL.
2. A mode-specific prompt asks Gemini for a bounded, actionable response.
3. Structured analysis responses are validated with Pydantic before reaching the UI.
4. Identical analysis requests are cached using the content, model, feature, and prompt
   version.
5. Daily per-user limits protect free-tier quota.
6. Provider timeouts, malformed JSON, quota exhaustion, and empty responses are handled.
7. Interview and coaching features provide deterministic fallbacks when appropriate.

### Feedback-driven personalization

Each coach response uses one of four strategies: direct action, structured plan,
diagnostic, or Socratic. Helpful/not-helpful feedback updates a per-user UCB1 policy for
that coaching mode. This changes which response strategy is preferred; it does not
fine-tune Gemini.

Weekly-plan bullets are converted into `coach_actions`. Completed actions and user-entered
outcomes become context for later advice, creating this loop:

```text
Profile → Plan → Action → Outcome → Updated coaching
```

## Database migrations

Apply all migrations:

```powershell
cd career-copilot-backend
python -m alembic upgrade head
```

Create a migration after changing SQLAlchemy models:

```powershell
python -m alembic revision --autogenerate -m "describe schema change"
python -m alembic check
```

For a database created by the former `Base.metadata.create_all()` workflow, run this once:

```powershell
python create_tables.py
```

It detects the legacy schema, stamps the baseline, and applies newer migrations.

## Testing and quality checks

Backend tests use an isolated SQLite database and mock live AI calls:

```powershell
cd career-copilot-backend
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

The suite covers authentication, authorization, cross-user isolation, application and
dashboard behavior, profiles, AI caching, provider quota behavior, non-résumé handling,
coach feedback, and trackable actions.

Build and type-check the frontend:

```powershell
cd career-copilot-frontend
npm run build
```

GitHub Actions runs both checks and validates a fresh Alembic migration on every push and
pull request. The human-reviewed AI rubric is stored in
`career-copilot-backend/evals/evaluation_cases.json`.

## Datadog APM

The backend includes `ddtrace` instrumentation for FastAPI requests, SQLAlchemy queries,
errors, and runtime metrics.

After creating a Datadog API key:

```powershell
$env:DD_API_KEY="your-datadog-api-key"
$env:DD_SITE="datadoghq.com"
docker compose --profile observability up -d datadog-agent
```

For a manually started backend:

```powershell
cd career-copilot-backend
$env:DD_SERVICE="career-copilot-backend"
$env:DD_ENV="development"
$env:DD_AGENT_HOST="127.0.0.1"
$env:DD_RUNTIME_METRICS_ENABLED="true"
$env:DD_LOGS_INJECTION="true"
ddtrace-run python -m uvicorn app.main:app --reload
```

The API key belongs only in the Agent environment and must never be committed.

## Production checklist

Before deploying:

- Set `ENV=production` and a random `SECRET_KEY` of at least 32 characters.
- Use a managed PostgreSQL database and run `alembic upgrade head` during release.
- Set the deployed frontend URL in `CORS_ORIGINS`.
- Set `NEXT_PUBLIC_API_URL` during the frontend build.
- Restrict and rotate Gemini, Supabase, and Datadog credentials.
- Confirm `/health/ready` succeeds from the hosting platform.
- Configure HTTPS; production cookies are marked secure automatically.
- Choose an AI daily limit appropriate for the Gemini project quota.
- Run backend tests, the frontend production build, and the AI evaluation rubric.
- Configure Datadog alerts for elevated error rate, latency, and failed readiness checks.

## Security notes

- Passwords are hashed with bcrypt.
- Authentication cookies are HTTP-only and use `SameSite=Lax`.
- Production cookies require HTTPS.
- Database records are filtered by authenticated user ownership.
- Upload size and supported document types are validated.
- AI and infrastructure secrets remain backend-only.
- AI-generated career advice may contain mistakes; users should verify important hiring
  and company-specific information.

## License

No license has been declared yet. Add a `LICENSE` file before distributing the project
outside its intended academic or portfolio use.
