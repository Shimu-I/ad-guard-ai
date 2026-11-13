# Backend

FastAPI app and PostgreSQL models for AdGuard AI.

## Run locally

From the repository root:

```
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r backend/requirements-dev.txt
cp .env.example .env               # then edit it
cd backend
uvicorn app.main:app --reload
```

Open http://localhost:8000/health and http://localhost:8000/docs.

If `DATABASE_URL` is not set, the app falls back to a local SQLite file so it still starts. For PostgreSQL, paste the connection string from Supabase or Neon; `postgresql://` and `postgres://` URLs are converted to the psycopg driver automatically.

## Run tests

From the repository root:

```
pytest
```

## Layout

```
app/config.py      settings from environment and .env
app/database.py    engine, session, declarative base
app/db_url.py      database URL helpers
app/models.py      Brand, Product, Ad, VerificationReport, VerificationCheck
app/main.py        FastAPI app factory
app/routers/       API routes (health for now)
```

## Notes

- Tables are created at startup for now. Alembic migrations replace this later.
- Brands and products are archived, not deleted, while ads still use them.
- An ad approval is tied to the exact ad content; editing the ad invalidates it.
- Verification results are `verified`, `issue_found` or `cannot_verify`. A report with no checks is never "verified".
