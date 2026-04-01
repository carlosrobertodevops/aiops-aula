# Secrets Rotation Checklist (Dev / Staging / Prod)

Checklist unico para os 3 subprojetos do workspace.

## Regras Gerais (todos os ambientes)

- [ ] Nunca commitar `.env` com valores reais.
- [ ] Usar apenas `.env.example` com placeholders (`CHANGE_ME`, `change-me-in-production`).
- [ ] Rotacionar segredos em incidente, troca de equipe, ou a cada 90 dias (prod).
- [ ] Aplicar principio de menor privilegio para usuarios de banco.
- [ ] Atualizar segredo primeiro e reiniciar workloads em janela controlada.
- [ ] Validar health checks apos rotacao.

## 1) projetinho (Django)

### Segredos

- `DJANGO_SECRET_KEY`

### Dev

- [ ] Copiar `projetinho/.env.example` para `.env` local.
- [ ] Definir `DJANGO_SECRET_KEY` forte localmente.
- [ ] Executar `DJANGO_SECRET_KEY=... python manage.py check`.

### Staging / Prod

- [ ] Definir `DJANGO_SECRET_KEY` no gerenciador de segredos/plataforma (nao em arquivo versionado).
- [ ] Reiniciar app Django para carregar o novo valor.
- [ ] Validar login/sessao e `python manage.py check` no ambiente.

## 2) kube-news (Node + Postgres)

### Segredos

- `DB_PASSWORD`
- `POSTGRES_PASSWORD`

### Dev (docker compose)

- [ ] Copiar `kube-news/.env.example` para `.env` local.
- [ ] Alterar `DB_PASSWORD` e `POSTGRES_PASSWORD` para valores fortes.
- [ ] Executar `docker compose config -q`.
- [ ] Subir stack e validar `GET /health` e `GET /ready`.

### Staging / Prod (Kubernetes)

- [ ] Atualizar `Secret` (`kube-news-secret`) com novos valores.
- [ ] Reiniciar deployment da app e do Postgres conforme estrategia do ambiente.
- [ ] Validar conectividade app->db e readiness/liveness.

## 3) boilerplate-aiops-na-pratica (FastAPI + Postgres)

### Segredos

- `DATABASE_URL` (usuario/senha do banco)
- `ANTHROPIC_API_KEY`
- `DISCORD_BOT_TOKEN` (quando habilitado)

### Dev

- [ ] Copiar `boilerplate-aiops-na-pratica/.env.example` para `.env` local.
- [ ] Definir `DATABASE_URL` e tokens reais no `.env` local (nao versionar).
- [ ] Executar `docker compose config -q` e validar subida dos servicos.

### Staging / Prod

- [ ] Injetar segredos via Secret Manager/CI/CD (nao hardcoded).
- [ ] Rotacionar `ANTHROPIC_API_KEY` e `DISCORD_BOT_TOKEN` com janela de validacao.
- [ ] Rotacionar credenciais do Postgres e atualizar `DATABASE_URL`.
- [ ] Reiniciar app e validar endpoints de health e fluxo principal.

## Passos de Rotacao Segura (ordem recomendada)

1. Gerar novo segredo.
2. Publicar novo segredo no ambiente alvo.
3. Reiniciar workloads dependentes.
4. Validar health/readiness e fluxo funcional minimo.
5. Revogar segredo antigo.
6. Registrar data da rotacao e responsavel.

## Evidencias Minimas por Rotacao

- Ambiente e servico afetado.
- Variavel/segredo rotacionado.
- Horario inicio/fim.
- Resultado dos checks (health/check/compose).
- Responsavel pela execucao.

## Runbook Operacional

## Matriz de Responsabilidade e Periodicidade

| Subprojeto | Segredo | Ambiente | Responsavel | Periodicidade | Ultima rotacao | Proxima rotacao |
|------------|---------|----------|-------------|---------------|----------------|-----------------|
| projetinho | `DJANGO_SECRET_KEY` | staging/prod | App Owner Django | 90 dias | PREENCHER | PREENCHER |
| kube-news | `DB_PASSWORD` | staging/prod | App Owner Node + DBA | 90 dias | PREENCHER | PREENCHER |
| kube-news | `POSTGRES_PASSWORD` | staging/prod | DBA/Platform | 90 dias | PREENCHER | PREENCHER |
| boilerplate-aiops-na-pratica | `DATABASE_URL` credenciais | staging/prod | App Owner AIOps + DBA | 90 dias | PREENCHER | PREENCHER |
| boilerplate-aiops-na-pratica | `ANTHROPIC_API_KEY` | staging/prod | App Owner AIOps | 90 dias ou incidente | PREENCHER | PREENCHER |
| boilerplate-aiops-na-pratica | `DISCORD_BOT_TOKEN` | staging/prod | App Owner AIOps | 90 dias ou incidente | PREENCHER | PREENCHER |

## Janela de Execucao

- Recomendado: janela de baixa demanda com rollback definido.
- Registrar ticket/change antes da execucao.
- Executar rotacao por ambiente (dev -> staging -> prod), nunca tudo ao mesmo tempo.

## Procedimento Operacional (por segredo)

1. Abrir ticket de mudanca com impacto, dono e janela.
2. Gerar novo valor no provedor de segredos.
3. Atualizar segredo no ambiente alvo.
4. Reiniciar apenas workloads dependentes.
5. Rodar verificacoes tecnicas do subprojeto.
6. Validar funcionalmente o fluxo minimo.
7. Revogar segredo antigo.
8. Atualizar a matriz com data da rotacao e proxima data.

## Comandos de Verificacao Rapida

- `projetinho`: `DJANGO_SECRET_KEY=... python manage.py check`
- `kube-news`: `docker compose config -q`
- `boilerplate-aiops-na-pratica`: `docker compose config -q`

## Registro de Rotacao (template)

| Data (UTC) | Subprojeto | Segredo | Ambiente | Responsavel | Ticket/Change | Resultado checks | Observacoes |
|------------|------------|---------|----------|-------------|---------------|------------------|-------------|
| PREENCHER | PREENCHER | PREENCHER | PREENCHER | PREENCHER | PREENCHER | PASS/FAIL | PREENCHER |
