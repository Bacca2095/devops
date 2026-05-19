# Project Management System

Internal system for managing projects, team members, and resource assignments in a technology outsourcing context.

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI · SQLAlchemy (async) · Alembic · Python 3.14 · uv |
| Frontend | React 19 · TypeScript · shadcn/ui · Vite · React Router · TanStack Query · Zustand |
| Database | PostgreSQL 16 |
| DevOps | Docker Compose · GitHub Actions · Railway · GHCR |

## Live Demo

| Service | URL |
|---|---|
| Frontend | https://frontend-production-5ef0.up.railway.app |

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

The ports are determined by `BACKEND_PORT` and `FRONTEND_PORT` in `.env` (defaults: `8000` and `3000`):

| Service | URL |
|---|---|
| Backend API | `http://localhost:{BACKEND_PORT}/docs` |
| Frontend | `http://localhost:{FRONTEND_PORT}` |

## Environment Variables

Copy `.env.example` to `.env` and complete the required values before starting any service.

| Variable | Used by | Required | Description |
|---|---|---|---|
| `DATABASE_HOST` | Backend | Yes | Postgres hostname (`localhost` without Docker, `database` inside Compose) |
| `DATABASE_PORT` | Backend / DB | Yes | Postgres port (default `5432`) |
| `DATABASE_NAME` | Backend / DB | Yes | Database name |
| `DATABASE_USER` | Backend / DB | Yes | Postgres user |
| `DATABASE_PASSWORD` | Backend / DB | Yes | Postgres password |
| `SECRET_KEY` | Backend | Yes | Secret for future JWT signing; must be a long random string in production |
| `DEBUG` | Backend | No | Enables debug mode and verbose error responses (default `false`) |
| `ALLOWED_ORIGINS` | Backend | No | JSON array of allowed CORS origins (default `["http://localhost:3000"]`) |
| `BACKEND_PORT` | Compose | No | Host port mapped to the backend container (default `8000`) |
| `FRONTEND_PORT` | Compose | No | Host port mapped to the frontend container (default `3000`) |
| `VITE_API_BASE_URL` | Frontend (dev only) | No | API base URL used by the browser in local development (`pnpm dev`). In production the frontend calls its own origin and Nginx handles the proxy; this variable is ignored. |
| `BACKEND_URL` | Nginx (prod only) | Yes | Backend URL that Nginx proxies `/api/` requests to inside the container (e.g. `http://backend:8000`). Not used in local development. |

## Local Setup (without Docker)

**Backend**

```bash
cd backend
uv sync --group dev
cp ../.env.example ../.env  # set DATABASE_HOST=localhost and SECRET_KEY
uv run alembic upgrade head
uv run fastapi dev main.py
```

**Frontend**

```bash
cd frontend
pnpm install
pnpm dev
```

## Tests

```bash
cd backend
uv run pytest
```

Coverage:

- **Domain entities** (`tests/unit/domain/`): status transitions for `ProjectEntity`, `AssignmentEntity`, `TeamMemberEntity`; validation rules for `TimeLogEntity`.
- **Use cases** (`tests/unit/use_cases/`): `CreateAssignment`, `CreateTimeLog`, `UpdateAssignmentStatus`. Repository dependencies are replaced with in-memory fakes.

## Frontend Screens

| Screen | Description |
|---|---|
| Project list | Paginated table with filters by Status and Priority, name search |
| Project detail | Info card, summary card, assignments table, add-assignment form, log-hours modal |
| Team member list | Paginated table with filters by Role, Seniority, Status |
| Team member detail | Info card and assignments history |
| Create / Edit project | Form with validation and backend error display |
| Create / Edit team member | Form with validation and backend error display |

## Architecture

The backend follows Clean Architecture with DDD principles across four layers:

```
backend/app/
├── api/
│   ├── dto/              # Pydantic request/response models
│   ├── routers/          # FastAPI routers — HTTP only
│   ├── dependencies/     # DI: use case instantiation
│   └── exception_handlers.py
│
├── application/
│   └── use_cases/        # One file per use case
│
├── domain/
│   ├── entity/           # Domain entities with business rules
│   ├── interfaces/       # Abstract repository contracts
│   ├── value_objects/    # Immutable domain types
│   └── exceptions/       # Typed domain exceptions
│
└── infrastructure/
    ├── models/           # SQLAlchemy ORM models
    ├── mappers/          # Bidirectional translation: ORM ↔ entity
    ├── repositories/     # Concrete repository implementations
    ├── config.py
    └── database.py
```

**Structural deviations:**

- `api/dto/`: DTOs are the standard DDD term for cross-boundary data carriers; "schema" is a validation concept.
- `application/use_cases/`: each command or query lives in its own file, enforcing SRP. `services/` is reserved for external integrations.
- `domain/entity/`: avoids ambiguity with ORM models.
- `domain/value_objects/`: encapsulates immutable domain concepts (filters, pagination) without leaking Pydantic types.
- `infrastructure/models/` and `infrastructure/mappers/`: domain entities remain pure Python dataclasses, decoupled from SQLAlchemy.

Frontend structure (organized by feature):

```
frontend/src/
├── api/        # Axios client and per-resource services
├── hooks/      # TanStack Query hooks per domain
├── pages/      # Route-level components
├── store/      # Zustand stores (persisted to localStorage)
├── types/      # TypeScript interfaces mirroring API DTOs
└── constants/  # Enum label maps
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET/POST` | `/api/projects/` | List / Create project |
| `GET/PUT/PATCH` | `/api/projects/{id}/` | Detail / Update / Status update |
| `GET` | `/api/projects/{id}/summary/` | Aggregated summary |
| `GET/POST` | `/api/projects/{id}/assignments/` | List / Create assignment |
| `PATCH` | `/api/assignments/{id}/status/` | Update status |
| `GET/POST` | `/api/assignments/{id}/timelogs/` | List / Log hours |
| `GET/POST` | `/api/team-members/` | List / Create member |
| `GET/PUT/PATCH` | `/api/team-members/{id}/` | Detail / Update / Toggle status |

## Database

Tables: `projects`, `team_members`, `assignments`, `time_logs`.

**Index decisions**

B-tree composite indexes are read left-to-right: a query that filters only on the second column cannot use the index. This drives the choice of leading column and explains why some standalone indexes are needed alongside composites.

`assignments(project_id, status)` — every project summary and assignment list query always scopes to a `project_id` first and frequently also filters by `status` (e.g. count active assignments). A composite with `project_id` as the leading column serves both access patterns in a single index, avoiding a full table scan on each summary request.

`time_logs(assignment_id, logged_date)` — time log queries are always scoped to a specific assignment and are ordered by `logged_date DESC`. The composite covers the filter and the sort in one scan without a separate sort step.

`projects(status, priority)` — the list endpoint supports filtering by status alone, by priority alone, or by both. A composite with `status` as the leading column covers status-only and status+priority queries. A separate `projects(priority)` index is required for priority-only queries because `status` is not the leading column there.

`projects(name)` — supports the name partial search. The current `ILIKE '%term%'` (leading wildcard) cannot use a B-tree index, so this index only helps with prefix searches. A `pg_trgm` GIN index would cover full substring search but requires the `pg_trgm` extension — left as a future improvement.

`team_members(role, seniority)` — same reasoning as `projects(status, priority)`: covers role-only (leading prefix) and role+seniority combined queries. Standalone `team_members(seniority)` and `team_members(status)` indexes are added for seniority-only and status-only queries respectively.

**Schema decisions:**

- Integer primary keys: simpler joins and better index performance at this scale.
- PostgreSQL native `ENUM` for status and role columns.
- `time_logs.description` nullable: enables fast hour logging.
- `assignment.end_date` and `project.end_date` nullable: ongoing assignments and open-ended projects are valid states.

## Architecture Decisions

**FastAPI over Laravel.** FastAPI's non-opinionated structure allows Clean Architecture and DDD to be applied without working around framework conventions. SQLAlchemy gives explicit control over query execution, transactions, and loading strategies, whereas Eloquent's Active Record pattern blurs the boundary between domain entities and persistence — a fundamental conflict with DDD's separation of concerns. Automatic OpenAPI documentation via Pydantic and strong typing at every layer boundary are additional factors.

**Async backend.** The stack runs on Uvicorn with `AsyncSession` and async repository methods. The event loop is never blocked by I/O, allowing a single worker to handle many concurrent requests. The trade-off is propagation of `await` through every layer and slightly more involved testing.

**Monorepo.** Backend and frontend share a single repository to simplify CI, Docker Compose orchestration, and environment management.

**Domain vs. application logic.** Rules that define *what is valid* live in the domain (entities, domain exceptions). Rules that define *how to execute an operation* live in the application layer (use cases). Example: assignment status transitions are validated inside `AssignmentEntity`; orchestrating fetch, validation, and persistence is the responsibility of `UpdateAssignmentStatusUseCase`.

**Repository pattern with interfaces.** Abstract repositories live in `domain/interfaces/`; concrete implementations in `infrastructure/repositories/`. Use cases depend only on the interface, allowing the persistence layer to be swapped without touching application or domain code.

## CI/CD

GitHub Actions runs on every push to `main`/`develop` and on pull requests to `main`:

- **backend-ci**: `ruff check` → `pytest` → build and push Docker image to GHCR.
- **frontend-ci**: `eslint` → `vite build` → build and push Docker image to GHCR.

Both jobs run in parallel. Images are tagged with the commit SHA and with `latest` (on `main`) or `develop` (on `develop`).

The CD workflow triggers on successful CI on `main` and deploys to Railway using the pre-built images, avoiding a redundant build on the deployment platform.

## Future Improvements

- **Authentication.** Add JWT-based auth with `python-jose`; `SECRET_KEY` is already wired into the config. All endpoints are currently public.
- **Soft deletes.** Replace hard deletes with a `deleted_at` column or an archive status so that project and assignment history is never lost on removal.
- **Date range validation on assignments.** Add a domain invariant that enforces `start_date ≤ end_date` before persisting.
- **Migrations as a pre-deploy step.** Move `alembic upgrade head` out of the container startup command and into a dedicated init container or a CI/CD pre-deploy job to avoid race conditions on multi-instance deployments.
- **Notification system.** Emit events (webhook or message queue) on assignment changes and hour logging so team members have visibility without polling.
- **Semantic image versioning.** Generate semver tags (`v1.2.3`) from Git tags in the CI pipeline alongside the existing commit SHA tags, enabling version-specific rollbacks and cleaner release tracking.
