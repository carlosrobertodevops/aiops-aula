# Technology Stack

**Analysis Date:** 2026-04-01

## Languages

**Primary:**
- Python 3.12+ - Backend/agent app in `boilerplate-aiops-na-pratica/src/my_agent_app/` (`requires-python = ">=3.12"` in `boilerplate-aiops-na-pratica/pyproject.toml`)

**Secondary:**
- JavaScript (Node.js) - Web app in `kube-news/src/` (`kube-news/src/server.js`, `kube-news/src/models/post.js`)
- HTML/EJS templates - Server-rendered views in `kube-news/src/views/*.ejs` and `boilerplate-aiops-na-pratica/src/my_agent_app/templates/*.html`

## Runtime

**Environment:**
- Python 3.12+ (`boilerplate-aiops-na-pratica/pyproject.toml`)
- Node.js 22 Alpine (`kube-news/src/Dockerfile`)

**Package Manager:**
- UV (Python project metadata/tooling in `boilerplate-aiops-na-pratica/pyproject.toml`)
- npm (Node app scripts/deps in `kube-news/src/package.json`)
- Lockfile: Present for Node (`kube-news/src/package-lock.json`), missing for Python (no `uv.lock` detected)

## Frameworks

**Core:**
- FastAPI - API/web backend app bootstrap in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`
- LangChain + Anthropic adapter - Agent execution in `boilerplate-aiops-na-pratica/src/my_agent_app/agents/root_cause_agent.py` and `boilerplate-aiops-na-pratica/src/my_agent_app/agents/fix_agent.py`
- Express 4.18 - HTTP app and routes in `kube-news/src/server.js`

**Testing:**
- Not detected (no Jest/Vitest/Pytest config files found in repository root)

**Build/Dev:**
- Uvicorn - ASGI runtime command documented in `boilerplate-aiops-na-pratica/README.md`
- Alembic - Database migrations in `boilerplate-aiops-na-pratica/alembic/` and `boilerplate-aiops-na-pratica/alembic.ini`
- Hatchling - Build backend in `boilerplate-aiops-na-pratica/pyproject.toml`
- Docker/Docker Compose - Container/runtime orchestration in `kube-news/src/Dockerfile`, `kube-news/docker-compose.yml`, and `boilerplate-aiops-na-pratica/docker-compose.yml`

## Key Dependencies

**Critical:**
- `fastapi[standard]` - API framework for agent service (`boilerplate-aiops-na-pratica/pyproject.toml`)
- `langchain[anthropic]` and `langchain-mcp-adapters` - LLM agent + MCP integration (`boilerplate-aiops-na-pratica/pyproject.toml`, `boilerplate-aiops-na-pratica/src/my_agent_app/agents/mcp_kubernetes.py`)
- `express` + `sequelize` + `pg` - Web/API + Postgres ORM/driver in `kube-news/src/package.json` and `kube-news/src/models/post.js`

**Infrastructure:**
- `sqlalchemy` + `asyncpg` - Async database access in `boilerplate-aiops-na-pratica/src/my_agent_app/database.py`
- `kubernetes` - Kubernetes event collection client in `boilerplate-aiops-na-pratica/src/my_agent_app/collector/event_collector.py`
- `httpx` - Outbound HTTP for Discord in `boilerplate-aiops-na-pratica/src/my_agent_app/notifications/discord.py`
- `express-prom-bundle` + `prom-client` - Metrics in `kube-news/src/server.js` and `kube-news/src/middleware.js`

## Configuration

**Environment:**
- Python app loads env via `load_dotenv()` in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`
- Node app reads env via `process.env` in `kube-news/src/models/post.js`
- Environment templates exist as `boilerplate-aiops-na-pratica/.env.example` and `kube-news/.env.example` (existence noted only)

**Build:**
- `boilerplate-aiops-na-pratica/pyproject.toml` (project/build/dependencies)
- `boilerplate-aiops-na-pratica/alembic.ini` + `boilerplate-aiops-na-pratica/alembic/env.py` (migration runtime)
- `kube-news/src/package.json` (scripts/deps)
- `kube-news/src/Dockerfile` (Node container image/runtime)

## Platform Requirements

**Development:**
- Python 3.12+ and UV for `boilerplate-aiops-na-pratica/` (`boilerplate-aiops-na-pratica/pyproject.toml`)
- Node.js/npm for `kube-news/src/` (`kube-news/src/package.json`)
- PostgreSQL reachable by env-based config (`boilerplate-aiops-na-pratica/src/my_agent_app/database.py`, `kube-news/src/models/post.js`)

**Production:**
- Containerized deployment on Kubernetes for Node service (`kube-news/k8s/deployment.yaml`, `kube-news/README.md`)
- Containerized deployment path for Python service via Docker Compose/K8s manifests (`boilerplate-aiops-na-pratica/docker-compose.yml`, `boilerplate-aiops-na-pratica/manifestos-k8s/*.yaml`)

---

*Stack analysis: 2026-04-01*
