# DSCC_CW_16817 - Study Planner (Django)

## Quick Start (Development)

1) Create `.env` (see `.env.production.example` for variable names)

2) Run with Docker:

```bash
docker compose up --build
```

App:
- http://localhost:8000

## Production-like Run (Nginx + Gunicorn)

This starts:
- `web` (Gunicorn + Django)
- `db` (PostgreSQL)
- `redis`
- `nginx` (reverse proxy + static/media)

1) Create `.env.production` from `.env.production.example`

2) Start:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

App:
- http://localhost

Health check:
- http://localhost/health/

## Notes

- Do not commit `.env` / `.env.production` (as they contain secrets).
- Database credentials for Django use `DB_*` variables.
- PostgreSQL container uses `POSTGRES_*` variables (they are both set in `.env.production`).
