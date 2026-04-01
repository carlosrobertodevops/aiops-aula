# External Integrations

**Analysis Date:** 2026-04-01

## APIs & External Services

**AI/Agent Services:**
- Anthropic Claude - LLM used by analysis/fix agents in `boilerplate-aiops-na-pratica/src/my_agent_app/agents/root_cause_agent.py` and `boilerplate-aiops-na-pratica/src/my_agent_app/agents/fix_agent.py`
  - SDK/Client: `langchain_anthropic.ChatAnthropic`
  - Auth: `ANTHROPIC_API_KEY` (documented in `boilerplate-aiops-na-pratica/CLAUDE.md`)

**MCP Tooling:**
- Kubernetes MCP Server - Tool server consumed by agents in `boilerplate-aiops-na-pratica/src/my_agent_app/agents/mcp_kubernetes.py`
  - SDK/Client: `langchain_mcp_adapters.client.MultiServerMCPClient`
  - Auth: URL-based endpoint via `MCP_KUBERNETES_URL`

**Cluster Platform API:**
- Kubernetes API - Warning events fetched in `boilerplate-aiops-na-pratica/src/my_agent_app/collector/event_collector.py`
  - SDK/Client: `kubernetes` Python client (`client.CoreV1Api`)
  - Auth: In-cluster config fallback to local kubeconfig (`config.load_incluster_config()`/`config.load_kube_config()`)

**Messaging/Notifications:**
- Discord REST API - Report notifications sent in `boilerplate-aiops-na-pratica/src/my_agent_app/notifications/discord.py`
  - SDK/Client: `httpx.AsyncClient`
  - Auth: `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID`

**Observability:**
- Prometheus scrape endpoint - Metrics middleware in `kube-news/src/server.js` and `kube-news/src/middleware.js`
  - SDK/Client: `express-prom-bundle`, `prom-client`
  - Auth: Not applied in app code (public `/metrics` route via Express stack)

## Data Storage

**Databases:**
- PostgreSQL (Python service)
  - Connection: `DATABASE_URL` (`boilerplate-aiops-na-pratica/src/my_agent_app/database.py`)
  - Client: SQLAlchemy async + `asyncpg` (`boilerplate-aiops-na-pratica/src/my_agent_app/database.py`)
- PostgreSQL (Node service)
  - Connection: `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_SSL_REQUIRE` (`kube-news/src/models/post.js`)
  - Client: Sequelize ORM + `pg` (`kube-news/src/models/post.js`, `kube-news/src/package.json`)

**File Storage:**
- Local filesystem only (static/templates in `kube-news/src/static/`, `boilerplate-aiops-na-pratica/src/my_agent_app/templates/`)

**Caching:**
- None detected in code/config (`boilerplate-aiops-na-pratica/src/`, `kube-news/src/`)

## Authentication & Identity

**Auth Provider:**
- Custom/service-token based integrations (no end-user auth provider detected)
  - Implementation: Environment-token auth for Discord (`DISCORD_BOT_TOKEN`) and implicit Anthropic key usage by SDK (`boilerplate-aiops-na-pratica/src/my_agent_app/agents/*.py`)

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry/Rollbar/NewRelic SDK imports in `boilerplate-aiops-na-pratica/src/` or `kube-news/src/`)

**Logs:**
- Python: standard `logging` in `boilerplate-aiops-na-pratica/src/my_agent_app/main.py`, `collector/event_collector.py`, `notifications/discord.py`
- Node: `console.log` in `kube-news/src/server.js`, `kube-news/src/middleware.js`

## CI/CD & Deployment

**Hosting:**
- Kubernetes manifests for Node app in `kube-news/k8s/deployment.yaml`
- Kubernetes manifests present for boilerplate workspace in `boilerplate-aiops-na-pratica/manifestos-k8s/*.yaml`
- Local container deployment via Docker Compose in `kube-news/docker-compose.yml` and `boilerplate-aiops-na-pratica/docker-compose.yml`

**CI Pipeline:**
- None detected (`.github/workflows/` not present)

## Environment Configuration

**Required env vars:**
- Python service: `DATABASE_URL`, `EVENT_COLLECTION_INTERVAL_MINUTES`, `AGENT_MAX_ITERATIONS`, `MCP_KUBERNETES_URL`, `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID`, `APP_BASE_URL` (`boilerplate-aiops-na-pratica/src/my_agent_app/*.py`)
- Node service: `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_SSL_REQUIRE` (`kube-news/src/models/post.js`)
- Anthropic key documented: `ANTHROPIC_API_KEY` (`boilerplate-aiops-na-pratica/CLAUDE.md`)

**Secrets location:**
- Local env templates present at `boilerplate-aiops-na-pratica/.env.example` and `kube-news/.env.example` (contents not read)
- Kubernetes secret resource documented in `kube-news/README.md` and manifests in `kube-news/k8s/deployment.yaml`

## Webhooks & Callbacks

**Incoming:**
- None detected (no webhook endpoint handlers identified in `boilerplate-aiops-na-pratica/src/my_agent_app/` or `kube-news/src/`)

**Outgoing:**
- Discord API message POSTs from `boilerplate-aiops-na-pratica/src/my_agent_app/notifications/discord.py`

---

*Integration audit: 2026-04-01*
