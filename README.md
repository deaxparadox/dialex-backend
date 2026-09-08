# Dialex backend

Django REST backend for Dialex (multi-agent debate/consensus system) — auth, case/debate data, Human Review, notifications.

Split out of the [Dialex monorepo](https://github.com/deaxparadox/Dialex) (`backend/`) with history preserved. Full design history (ADRs, specs, PRD, API/FLOWS docs) stays in that repo — this one is code only.

## Running (standalone, without docker-compose)

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values; DATABASE_URL must point at a real Postgres
cd src
python manage.py migrate
python manage.py runserver
```

For the full stack (Postgres, Redis, Temporal, the orchestrator) via docker-compose, see the Dialex monorepo — this repo doesn't carry that compose config.

## Apps

One app per bounded concern:

- `accounts` — custom `User` model, JWT auth
- `cases` — `Case`, `CaseTypeConfig`
- `debates` — `AgentPersona`, `Debate`, `DebateParticipant`, `Argument`, `ConvergenceCheck`, `Verdict`, `ResearchFinding`
- `consultations` — `ConsultationSession`, `ConsultationTurn`
- `reviews` — `HumanReview`
- `notifications` — `Notification`
