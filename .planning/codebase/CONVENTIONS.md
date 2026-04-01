# Coding Conventions

**Analysis Date:** 2026-04-01

## Naming Patterns

**Files:**
- Python modules use `snake_case.py` inside Django apps and FastAPI package (examples: `projetinho/accounts/views.py`, `projetinho/teams/models.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/web/router.py`).
- JavaScript backend files use lower-case names with dashes only where already present (examples: `kube-news/src/server.js`, `kube-news/src/system-life.js`).

**Functions:**
- Python functions and methods use `snake_case` (`projetinho/accounts/forms.py`, `projetinho/projects/views.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`).
- JavaScript functions use `camelCase` (`kube-news/src/models/post.js` with `strToBool`, `initDatabase`).

**Variables:**
- Constants are uppercase in Python and JS (`DEFAULT_INTERVAL_MINUTES` in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`, `DB_DATABASE` in `kube-news/src/models/post.js`).
- Local variables follow `snake_case` in Python and `camelCase` in JS.

**Types:**
- Python typing is partial; use explicit type hints for async/session helpers and IDs where present (`boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/web/router.py`).
- Django app (`projetinho/*`) does not use type annotations consistently.

## Code Style

**Formatting:**
- Tool used: Not detected (no `.prettierrc*`, `biome.json`, `ruff.toml`, `.flake8`, `pyproject` formatter sections).
- Key settings: Not applicable.

**Linting:**
- Tool used: Not detected (no `.eslintrc*`, `eslint.config.*`, or Python linter config).
- Key rules: Not applicable.

## Import Organization

**Order:**
1. Standard library imports first (`projetinho/kanban/settings.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`).
2. Framework/third-party imports second (`django.*`, `fastapi`, `sqlalchemy`, `markdown`).
3. Local app imports last (`accounts.*`, `teams.*`, `my_agent_app.*`).

**Path Aliases:**
- Not detected. Imports use package/module paths directly (`from projects.models import Project`, `from my_agent_app.models.report import Report`).

## Error Handling

**Patterns:**
- Django app favors framework defaults (403/404 handling via mixins/queryset filtering) and explicit guard checks in views (`projetinho/projects/views.py`, `projetinho/teams/views.py`).
- FastAPI app uses `try/except` around async DB and background tasks plus logging on failures (`boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/web/router.py`).
- JS app currently has minimal defensive handling in routes (`kube-news/src/server.js`).

## Logging

**Framework:** Python `logging` in FastAPI; `console.log` in JS app.

**Patterns:**
- Initialize logger once and reuse per module (`boilerplate-aiops-na-pratica/src/my_agent_app/main.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`).
- Log exceptions with contextual identifiers (report ID) in async flows (`boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`).
- Avoid new `console.log` in Python/Django code; current JS app still uses direct console output (`kube-news/src/server.js`, `kube-news/src/models/post.js`).

## Comments

**When to Comment:**
- Inline comments are sparse and mostly for guard/business-rule clarifications (`projetinho/accounts/views.py`, `projetinho/teams/tests.py`).
- Prefer self-descriptive class/function names and concise docstrings on mixins when access rules are non-trivial (`projetinho/projects/views.py`).

**JSDoc/TSDoc:**
- Not used.

## Function Design

**Size:**
- Django class-based views keep logic in small overridable methods (`get_queryset`, `form_valid`, `get_context_data`) in `projetinho/accounts/views.py`, `projetinho/projects/views.py`, `projetinho/teams/views.py`.
- FastAPI router keeps larger endpoint functions plus helper coroutines (`_run_fix`, `_get_session`) in `boilerplate-aiops-na-pratica/src/my_agent_app/api/router.py`.

**Parameters:**
- Request-driven handlers accept `request` + route params (`pk`, `team_pk`, `report_id`) and read validated form/model state from framework objects.

**Return Values:**
- Django views return redirect/response objects and rely on side effects via ORM/messages.
- FastAPI handlers return dict/`JSONResponse`/template responses explicitly.

## Module Design

**Exports:**
- Python modules export classes/functions by declaration; no explicit `__all__` usage detected.
- JS modules export via `exports.*` object members (`kube-news/src/models/post.js`).

**Barrel Files:**
- Limited usage through package `__init__.py` placeholders (`projetinho/*/__init__.py`, `boilerplate-aiops-na-pratica/src/my_agent_app/*/__init__.py`), not as centralized export barrels.

---

*Convention analysis: 2026-04-01*
