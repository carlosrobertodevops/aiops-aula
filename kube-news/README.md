# KubeNews

Plataforma de gerenciamento de notícias construída com Node.js e Express, projetada para execução em ambientes Kubernetes. Permite criar, listar e visualizar posts/notícias com armazenamento em PostgreSQL e métricas integradas via Prometheus.

## Stack

- **Runtime:** Node.js 22 (Alpine)
- **Framework:** Express.js 4.18
- **Template Engine:** EJS
- **Banco de Dados:** PostgreSQL 16 (via Sequelize ORM)
- **Monitoramento:** Prometheus (express-prom-bundle + prom-client)
- **Container:** Docker + Docker Compose
- **Orquestração:** Kubernetes

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DB_DATABASE` | `kubedevnews` | Nome do banco de dados |
| `DB_USERNAME` | `kubedevnews` | Usuário do banco |
| `DB_PASSWORD` | `CHANGE_ME` | Senha do banco (defina no `.env`/Secret) |
| `DB_HOST` | `localhost` | Host do PostgreSQL (em compose/k8s use `postgres`) |
| `DB_PORT` | `5432` | Porta do PostgreSQL |
| `DB_SSL_REQUIRE` | `false` | Habilitar SSL na conexão |

Variáveis do container Postgres (compose/k8s):

| Variável | Padrão |
|----------|--------|
| `POSTGRES_DB` | `kubedevnews` |
| `POSTGRES_USER` | `kubedevnews` |
| `POSTGRES_PASSWORD` | `CHANGE_ME` |

## Como Executar com Docker Compose

```bash
cp .env.example .env
docker compose up -d
```

A aplicação estará disponível em `http://localhost:8080`.

O Compose sobe dois serviços:
- **kube-news** — aplicação na porta 8080
- **postgres** — banco de dados na porta 5432 com volume persistente

O serviço do banco possui health check configurado. A aplicação só inicia após o PostgreSQL estar pronto.

Para parar:

```bash
docker compose down
```

## Como Fazer Deploy no Kubernetes

Todos os manifests estão no arquivo `k8s/deployment.yaml` e incluem: Secret, PersistentVolumeClaim, Deployments e Services para o PostgreSQL e a aplicação.

```bash
kubectl apply -f k8s/deployment.yaml
```

Recursos criados:
- **Secret** `kube-news-secret` — credenciais do banco
- **PVC** `postgres-pvc` — 1Gi de armazenamento para o PostgreSQL
- **Deployment** PostgreSQL — 1 réplica com probes de saúde
- **Deployment** KubeNews — 2 réplicas com probes de saúde
- **Service** PostgreSQL — ClusterIP na porta 5432
- **Service** KubeNews — LoadBalancer na porta 80 → 8080

A aplicação roda como usuário não-root com filesystem read-only.

## Endpoints Disponíveis

### Aplicação

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial com listagem de posts |
| GET | `/post` | Formulário de criação de post |
| POST | `/post` | Salvar novo post |
| GET | `/post/:id` | Visualizar post individual |
| POST | `/api/post` | Criação de posts em lote (JSON) |

### Sistema

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check — retorna estado e hostname |
| GET | `/ready` | Readiness check — 200 se pronto, 500 se não |
| PUT | `/unhealth` | Marca o serviço como não saudável |
| PUT | `/unreadyfor/:seconds` | Marca como não pronto por N segundos |
| GET | `/metrics` | Métricas Prometheus |

## Estrutura do Projeto

```
kube-news/
├── k8s/
│   └── deployment.yaml            # Manifests Kubernetes
├── src/
│   ├── Dockerfile                 # Imagem Docker da aplicação
│   ├── .dockerignore
│   ├── server.js                  # Entrada principal (Express + rotas)
│   ├── system-life.js             # Rotas de health/readiness
│   ├── middleware.js              # Middleware de contagem de requests
│   ├── package.json
│   ├── models/
│   │   └── post.js                # Modelo Sequelize + config do banco
│   ├── views/
│   │   ├── index.ejs              # Listagem de posts
│   │   ├── edit-news.ejs          # Formulário de criação
│   │   ├── view-news.ejs          # Visualização de post
│   │   └── partial/
│   │       ├── header.ejs
│   │       └── footer.ejs
│   └── static/
│       ├── img/                   # Imagens e ícones
│       └── styles/                # CSS
├── docker-compose.yml             # Compose com app + postgres
├── popula-dados.http              # Exemplos de requests para popular dados
└── .gitignore
```
