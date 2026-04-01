# Codebase Structure

**Analysis Date:** 2026-04-01

## Directory Layout

```text
aiops-aula/
├── boilerplate-aiops-na-pratica/   # FastAPI + async agent platform
├── kube-news/                      # Express + EJS + Postgres app
├── projetinho/                     # Django project management app
├── openspec/                       # Repository-level specs and changes
├── prompts/                        # Prompt engineering reference material
├── docs-test/                      # Generated docs/artifacts for study
├── excalidraw/                     # Diagram source files
└── .planning/codebase/             # Generated codebase mapping docs
```

## Directory Purposes

**`boilerplate-aiops-na-pratica/`:**
- Purpose: FastAPI service that collects Kubernetes events and generates/fixes reports.
- Contains: Python package, Alembic migrations, templates, Kubernetes manifests.
- Key files: `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/collector/event_collector.py`, `boilerplate-aiops-na-pratica/pyproject.toml`.

**`kube-news/`:**
- Purpose: Node.js web app for news posts with Prometheus metrics and health endpoints.
- Contains: Express server, Sequelize model, EJS views, static assets, deployment manifests.
- Key files: `kube-news/src/server.js`, `kube-news/src/system-life.js`, `kube-news/src/models/post.js`, `kube-news/src/package.json`, `kube-news/k8s/deployment.yaml`.

**`projetinho/`:**
- Purpose: Django app for user/team/project management.
- Contains: Django project config, domain apps, templates, migrations, OpenSpec docs.
- Key files: `projetinho/manage.py`, `projetinho/kanban/settings.py`, `projetinho/kanban/urls.py`, `projetinho/accounts/models.py`, `projetinho/teams/models.py`, `projetinho/projects/models.py`.

**`openspec/`:**
- Purpose: top-level spec/change tracking for repository workflow.
- Contains: `openspec/config.yaml`, `openspec/changes/`, `openspec/specs/`.
- Key files: `openspec/config.yaml`.

**`prompts/`:**
- Purpose: documentation and examples for prompting workflows.
- Contains: Markdown prompt guides.
- Key files: `prompts/01-engenharia-prompts.md`, `prompts/02-prompts-claude-code.md`.

## Key File Locations

**Entry Points:**
- `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`: FastAPI app bootstrap + lifecycle.
- `kube-news/src/server.js`: Express app bootstrap + route wiring.
- `projetinho/manage.py`: Django command entry point.

**Configuration:**
- `boilerplate-aiops-na-pratica/pyproject.toml`: Python package/runtime dependencies.
- `kube-news/src/package.json`: Node dependencies and start script.
- `projetinho/kanban/settings.py`: Django installed apps, middleware, database, auth config.

**Core Logic:**
- `boilerplate-aiops-na-pratica/src/my_agent_app/collector/`: event ingestion/dedup/analysis orchestration.
- `boilerplate-aiops-na-pratica/src/my_agent_app/agents/`: LangChain + MCP agent executions.
- `kube-news/src/models/post.js`: Sequelize model and DB initialization.
- `projetinho/accounts/`, `projetinho/teams/`, `projetinho/projects/`: domain models, URLs, views, forms.

**Testing:**
- `projetinho/accounts/tests.py`, `projetinho/teams/tests.py`, `projetinho/projects/tests.py`, `projetinho/core/tests.py`.
- Not detected: dedicated test suites in `kube-news/src/` and `boilerplate-aiops-na-pratica/src/my_agent_app/`.

## Naming Conventions

**Files:**
- Python modules use `snake_case.py` (example: `boilerplate-aiops-na-pratica/src/my_agent_app/collector/event_handler.py`).
- Django app modules follow framework conventions (`models.py`, `views.py`, `urls.py`, `forms.py`) under `projetinho/*/`.
- Node modules in `kube-news/src/` use lower-case JS filenames (`server.js`, `system-life.js`, `middleware.js`).

**Directories:**
- Python package domains use lower-case directories (example: `boilerplate-aiops-na-pratica/src/my_agent_app/agents/`).
- Django apps are top-level plural nouns (`projetinho/accounts/`, `projetinho/teams/`, `projetinho/projects/`).
- Frontend templates are grouped by domain (`projetinho/templates/accounts/`, `projetinho/templates/teams/`, `kube-news/src/views/partial/`).

## Where to Add New Code

**New feature (FastAPI agent app):**
- Primary code: `boilerplate-aiops-na-pratica/src/my_agent_app/`.
- API endpoints: `boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`.
- UI pages/templates: `boilerplate-aiops-na-pratica/src/my_agent_app/web/router.py` and `boilerplate-aiops-na-pratica/src/my_agent_app/templates/`.
- Persistence/migrations: models in `boilerplate-aiops-na-pratica/src/my_agent_app/models/`, migrations in `boilerplate-aiops-na-pratica/alembic/versions/`.

**New feature (Express kube-news app):**
- Route handlers: `kube-news/src/server.js` (current pattern is centralized).
- Domain model updates: `kube-news/src/models/post.js`.
- HTML updates: `kube-news/src/views/` and assets in `kube-news/src/static/`.

**New feature (Django projetinho):**
- Choose domain app first: `projetinho/accounts/`, `projetinho/teams/`, or `projetinho/projects/`.
- Add model/form/view/url in that app and wire route in `projetinho/kanban/urls.py` if needed.
- Add templates under matching path in `projetinho/templates/<app>/`.
- Add/extend tests in corresponding `projetinho/<app>/tests.py`.

**New Component/Module:**
- FastAPI integrations/agents: `boilerplate-aiops-na-pratica/src/my_agent_app/agents/`.
- FastAPI collectors/processing: `boilerplate-aiops-na-pratica/src/my_agent_app/collector/`.
- Django reusable permissions/mixins: `projetinho/accounts/mixins.py` or app-specific module near target views.

**Utilities:**
- FastAPI shared infra helpers: `boilerplate-aiops-na-pratica/src/my_agent_app/database.py` and sibling modules in package root.
- Express shared middleware: `kube-news/src/middleware.js` or new file under `kube-news/src/`.
- Django shared validation/auth helpers: `projetinho/accounts/validators.py`, `projetinho/accounts/managers.py`, `projetinho/accounts/mixins.py`.

## Special Directories

**`.planning/codebase/`:**
- Purpose: generated architecture/stack/convention mapping docs.
- Generated: Yes.
- Committed: Yes (intended for planning workflows).

**`node-compile-cache/`:**
- Purpose: local runtime cache artifacts.
- Generated: Yes.
- Committed: Yes (currently present in repository tree).

**`projetinho/.venv/`:**
- Purpose: local Python virtual environment.
- Generated: Yes.
- Committed: No (development-local dependency environment).

**`docs-test/` and `excalidraw/`:**
- Purpose: documentation outputs and diagrams, not runtime application code.
- Generated: Mixed.
- Committed: Yes.

---

*Structure analysis: 2026-04-01*
