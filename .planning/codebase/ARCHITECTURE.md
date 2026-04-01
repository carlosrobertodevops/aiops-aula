# Architecture

**Analysis Date:** 2026-04-01

## Pattern Overview

**Overall:** Multi-application repository (workspace-style) with three independent web systems:
- FastAPI async agent platform in `boilerplate-aiops-na-pratica/src/my_agent_app/`
- Express + EJS web app in `kube-news/src/`
- Django MVC app in `projetinho/`

**Key Characteristics:**
- Runtime boundaries are explicit per app: Python/FastAPI (`boilerplate-aiops-na-pratica/src/my_agent_app/main.py`), Node/Express (`kube-news/src/server.js`), Django (`projetinho/manage.py`, `projetinho/kanban/settings.py`).
- Each app owns its own routing, persistence, and templates.
- The repository root is coordination/documentation oriented (`openspec/`, `prompts/`, `docs-test/`) rather than a single deployable service.

## Layers

**Workspace Layer:**
- Purpose: host multiple independent projects and shared planning assets.
- Location: repository root `.`
- Contains: project folders, agent tooling metadata, planning docs.
- Depends on: per-project tooling and configs.
- Used by: contributors and automation commands.

**FastAPI Agent App Layer (`boilerplate-aiops-na-pratica`):**
- Purpose: ingest Kubernetes Warning events, create analysis reports, trigger optional auto-fix.
- Location: `boilerplate-aiops-na-pratica/src/my_agent_app/`
- Contains:
  - App bootstrap/lifecycle in `main.py`
  - HTTP API in `api/router.py`
  - HTML web routes in `web/router.py`
  - Collector pipeline in `collector/event_collector.py` and `collector/event_handler.py`
  - Agent orchestration in `agents/root_cause_agent.py` and `agents/fix_agent.py`
  - DB model in `models/report.py`
- Depends on: FastAPI, SQLAlchemy async, LangChain + MCP tools, Anthropic model, optional Discord API.
- Used by: operations users through `/api/*` and `/reports*` routes.

**Express App Layer (`kube-news`):**
- Purpose: CRUD-like news publishing UI/API with observability and health endpoints.
- Location: `kube-news/src/`
- Contains:
  - App entry and routes in `server.js`
  - Health/readiness router + middleware in `system-life.js`
  - Metrics middleware in `middleware.js`
  - Sequelize model/connection in `models/post.js`
  - EJS views in `views/`
- Depends on: Express, Sequelize/Postgres, Prometheus middleware.
- Used by: browser users and API clients (`/api/post`).

**Django App Layer (`projetinho`):**
- Purpose: team/project/user management with role-based permissions.
- Location: `projetinho/`
- Contains:
  - Django project bootstrap in `manage.py`, `kanban/settings.py`, `kanban/urls.py`
  - Domain apps: `accounts/`, `teams/`, `projects/`, `core/`
  - App routes in `accounts/urls.py`, `teams/urls.py`, `projects/urls.py`
  - Class-based views and mixin-based access control in `accounts/views.py`, `teams/views.py`, `projects/views.py`
  - Relational models in `accounts/models.py`, `teams/models.py`, `projects/models.py`
- Depends on: Django auth/session/template stack and SQLite (`kanban/settings.py`).
- Used by: authenticated browser users.

## Data Flow

**FastAPI event analysis flow:**

1. App starts and installs async DB sessionmaker and periodic collector in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`.
2. Collector fetches Kubernetes Warning events, filters by time window, transforms payloads in `collector/event_collector.py`.
3. Handler deduplicates by event UID against `reports.event_uids`, creates `Report`, runs analysis task in `collector/event_handler.py` with persistence in `models/report.py`.

**FastAPI fix execution flow:**

1. Client requests `POST /api/reports/{report_id}/fix` in `api/router.py`.
2. Route validates report status and marks `CORRIGINDO`.
3. Background task executes fix agent, persists `fix_result` + final status, then sends Discord notification in `api/router.py` + `notifications/discord.py`.

**Express publish flow:**

1. Request traverses request counter + Prometheus middleware + health gate in `kube-news/src/server.js`.
2. Route handlers validate incoming form payload and call `Post.create` / `Post.findAll` / `Post.findByPk`.
3. Response renders EJS templates in `kube-news/src/views/` or returns JSON for `/api/post`.

**Django management flow:**

1. Root URL dispatches to app URLConfs in `projetinho/kanban/urls.py`.
2. Class-based views enforce login/role checks using mixins (`accounts/views.py`, `projects/views.py`, `teams/views.py`).
3. ORM relationships (`Team`, `TeamMembership`, `Project`, custom `User`) constrain visibility and mutation scope (`teams/models.py`, `projects/models.py`, `accounts/models.py`).

**State Management:**
- FastAPI app state stores DB session factory in `app.state.sessionmaker` (`boilerplate-aiops-na-pratica/src/my_agent_app/main.py`).
- Express in-memory liveness/readiness flags are module-level variables in `kube-news/src/system-life.js`.
- Django state is DB-backed with session/auth middleware configured in `projetinho/kanban/settings.py`.

## Key Abstractions

**Report lifecycle abstraction (FastAPI):**
- Purpose: represent analysis/fix processing state transitions.
- Examples: `boilerplate-aiops-na-pratica/src/my_agent_app/models/report.py`, `collector/event_handler.py`, `api/router.py`.
- Pattern: status-driven workflow (`EM_ANALISE` → `COMPLETO/INCOMPLETO` → `CORRIGINDO` → `CORRIGIDO/FALHA_CORRECAO`).

**Health gate abstraction (Express):**
- Purpose: centralize liveness/readiness behavior.
- Examples: `kube-news/src/system-life.js`, integration in `kube-news/src/server.js`.
- Pattern: exported router + middleware module injected early in app pipeline.

**Role + membership authorization abstraction (Django):**
- Purpose: authorize operations by global role and per-team manager membership.
- Examples: `projetinho/accounts/models.py`, `projetinho/teams/models.py`, `projetinho/projects/views.py`.
- Pattern: `User.is_admin`/`is_manager` properties plus query-based permission checks.

## Entry Points

**FastAPI HTTP app:**
- Location: `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`
- Triggers: ASGI startup via `uvicorn my_agent_app.main:app`.
- Responsibilities: initialize app, routers, DB engine, periodic collection task.

**Express HTTP app:**
- Location: `kube-news/src/server.js`
- Triggers: Node start script (`kube-news/src/package.json` → `node server.js`).
- Responsibilities: register middleware/routes, initialize Sequelize schema, listen on port 8080.

**Django command app:**
- Location: `projetinho/manage.py`
- Triggers: `python manage.py <command>`.
- Responsibilities: set settings module and delegate command execution.

## Error Handling

**Strategy:** Localized try/except with graceful degradation plus logging.

**Patterns:**
- FastAPI web routes return template-based error pages on DB failures in `boilerplate-aiops-na-pratica/src/my_agent_app/web/router.py`.
- FastAPI background tasks catch and log exceptions, then update report status defensively in `collector/event_handler.py` and `api/router.py`.
- Express routes mostly rely on direct async handlers with inline validation in `kube-news/src/server.js`.
- Django views use guard checks + redirects/messages and explicit forbidden responses in `projetinho/projects/views.py` and `projetinho/teams/views.py`.

## Cross-Cutting Concerns

**Logging:**
- Python services use module loggers and `logging.basicConfig(level=logging.INFO)` in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`.
- Express uses `console.log` in request middleware and API handler (`kube-news/src/middleware.js`, `kube-news/src/server.js`).
- Django feedback uses `django.contrib.messages` in app views (`projetinho/accounts/views.py`, `projetinho/projects/views.py`, `projetinho/teams/views.py`).

**Validation:**
- FastAPI validates fix workflow by report existence/status in `boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`.
- Express validates field lengths manually in `kube-news/src/server.js` before persistence.
- Django validation relies on forms and model constraints referenced in view classes (`projetinho/accounts/views.py`, `projetinho/projects/views.py`, `projetinho/teams/views.py`).

**Authentication:**
- FastAPI routes currently expose API/web endpoints without auth middleware (`boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`, `web/router.py`).
- Express app currently has no user auth layer in `kube-news/src/server.js`.
- Django enforces login and role-based access through built-in auth middleware and mixins (`projetinho/kanban/settings.py`, `projetinho/accounts/views.py`, `projetinho/projects/views.py`, `projetinho/teams/views.py`).

---

*Architecture analysis: 2026-04-01*
