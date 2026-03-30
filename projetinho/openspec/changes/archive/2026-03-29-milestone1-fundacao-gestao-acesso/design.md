## Context

A empresa usa Google Sheets para gerenciar projetos e tarefas de 6 times (~40 pessoas). Uma tentativa com Jira falhou por complexidade. Este milestone cria a fundação do sistema: autenticação, times e projetos, usando Django com server-side rendering e Bootstrap.

O repositório está vazio — não há código existente. Tudo será criado do zero.

## Goals / Non-Goals

**Goals:**
- Estrutura do projeto Django pronta para crescer nos próximos milestones
- Autenticação funcional com email/senha e três papéis de acesso
- CRUD completo de times e projetos com isolamento de visibilidade
- Testes automatizados cobrindo models, views e permissões
- Interface funcional com Bootstrap (não precisa ser bonita, precisa ser usável)

**Non-Goals:**
- Deploy em Kubernetes ou qualquer infraestrutura
- CI/CD pipeline
- Kanban board (Milestone 2)
- Dashboard gerencial (Milestone 3)
- Integrações com Slack ou GitHub (Milestones 4 e 5)
- PostgreSQL — usaremos SQLite para desenvolvimento

## Decisions

### 1. Custom User Model com AbstractUser

**Decisão:** Estender `AbstractUser` com `USERNAME_FIELD = 'email'`.

**Alternativa considerada:** `AbstractBaseUser` — oferece controle total, mas exige reimplementar toda a lógica de autenticação do Django (permissões, admin, etc). Para um sistema interno com necessidades simples, o overhead não se justifica.

**Rationale:** O PRD exige login por email. O Django usa `username` por padrão e mudar isso depois de criar migrations é extremamente doloroso. `AbstractUser` mantém compatibilidade com o ecossistema Django (admin, decorators de permissão) enquanto permite customização suficiente.

### 2. Estrutura de Apps Django

**Decisão:** 4 apps Django:

```
kanban/                    # projeto Django (settings, urls, wsgi)
├── accounts/              # User model, autenticação, gestão de usuários
├── teams/                 # Times e memberships
├── projects/              # Projetos vinculados a times
└── core/                  # Templates base, template tags, mixins compartilhados
```

**Alternativa considerada:** App única para tudo — mais simples inicialmente, mas cresce rápido e dificulta manutenção quando os milestones 2-5 chegarem.

**Rationale:** Cada app mapeia para um domínio claro do PRD. Mantém separação de responsabilidades e facilita a adição do kanban board no Milestone 2 como uma nova app.

### 3. Modelo de Permissões

**Decisão:** Usar o campo `role` no User model (choices: `admin`, `manager`, `member`) + mixins customizados para views.

```
┌─────────────────────────────────────────────────────────┐
│                    MODELO DE ACESSO                      │
├──────────┬──────────────────────────────────────────────┤
│  Admin   │ Vê tudo. Gerencia usuários e times.          │
│  Gestor  │ Vê times que gerencia. Gerencia projetos.    │
│  Membro  │ Vê projetos dos seus times.                  │
└──────────┴──────────────────────────────────────────────┘

Visibilidade:
  Admin ──▶ todos os times e projetos
  Gestor ──▶ times onde é gestor
  Membro ──▶ times onde é membro
```

**Alternativa considerada:** Sistema de permissões do Django (`django.contrib.auth.permissions`) — muito granular para 3 papéis fixos. Adicionaria complexidade sem benefício.

**Rationale:** O PRD define exatamente 3 papéis com regras claras. Um campo choice + mixins é mais explícito e fácil de entender do que permissões genéricas.

### 4. TeamMembership como modelo intermediário

**Decisão:** Relação M2M entre User e Team via modelo `TeamMembership` explícito, com campo `is_manager`.

```python
# Estrutura conceitual
User ──M2M──▶ Team (via TeamMembership)
TeamMembership: user, team, is_manager (bool)
```

**Alternativa considerada:** `ManyToManyField` simples + lista separada de gestores — duplicaria informação e criaria risco de inconsistência.

**Rationale:** O PRD exige que cada time tenha pelo menos um gestor. Um modelo intermediário permite armazenar essa informação na relação e aplicar validações diretamente.

### 5. Frontend com Bootstrap via CDN

**Decisão:** Bootstrap 5 via CDN, sem build tools (npm, webpack, etc).

**Alternativa considerada:** Tailwind CSS — exigiria configuração de build pipeline, o que contradiz a decisão de manter tudo simples.

**Rationale:** Para ~40 usuários internos, Bootstrap via CDN elimina qualquer pipeline de build frontend. Templates Django + Bootstrap é uma combinação consagrada e produtiva.

### 6. Estrutura de templates

```
templates/
├── base.html              # Layout base: navbar, mensagens, Bootstrap
├── accounts/
│   ├── login.html
│   ├── user_list.html
│   ├── user_form.html
│   └── user_detail.html
├── teams/
│   ├── team_list.html
│   ├── team_form.html
│   └── team_detail.html
└── projects/
    ├── project_list.html
    ├── project_form.html
    └── project_detail.html
```

## Risks / Trade-offs

**SQLite em dev vs PostgreSQL em produção** → Há diferenças de comportamento entre os dois (ex: case sensitivity, JSON fields). Mitigação: evitar features específicas de PostgreSQL neste milestone. A migração para PostgreSQL será feita antes do deploy.

**Custom User Model precisa ser definido antes da primeira migration** → Se esquecermos, migrar depois é doloroso e envolve recrear o banco. Mitigação: é a primeira coisa a implementar.

**Bootstrap via CDN depende de internet** → Em ambiente corporativo fechado, pode ser um problema. Mitigação: se necessário no futuro, baixar os assets e servir como static files.

**Sem validação de email real** → O sistema aceita qualquer string como email. Mitigação: suficiente para sistema interno onde o admin cadastra os usuários. Validação de domínio pode ser adicionada futuramente se necessário.
