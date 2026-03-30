## 1. Setup do Projeto Django

- [x] 1.1 Criar projeto Django `kanban` com `django-admin startproject`
- [x] 1.2 Criar apps: `accounts`, `teams`, `projects`, `core`
- [x] 1.3 Configurar `settings.py`: apps instaladas, SQLite, templates dir, static files, session timeout (8h), `AUTH_USER_MODEL`
- [x] 1.4 Criar template base (`base.html`) com Bootstrap 5 via CDN, navbar e bloco de mensagens

## 2. App Accounts — User Model e Autenticação

- [x] 2.1 Implementar Custom User model (AbstractUser, email como USERNAME_FIELD, campo role com choices admin/manager/member)
- [x] 2.2 Implementar Custom UserManager (create_user, create_superuser sem username)
- [x] 2.3 Criar e rodar migrations iniciais
- [x] 2.4 Implementar validador de senha customizado (mínimo 8 chars, pelo menos uma letra e um número)
- [x] 2.5 Implementar view e template de login (email + senha, mensagens genéricas, tratamento de conta desativada)
- [x] 2.6 Implementar logout
- [x] 2.7 Implementar views de gestão de usuários (CRUD) — apenas admin: listar, criar, editar, desativar/reativar
- [x] 2.8 Implementar proteção contra desativação do último admin
- [x] 2.9 Implementar reset de senha por admin
- [x] 2.10 Implementar mixins de permissão: AdminRequiredMixin, ManagerRequiredMixin
- [x] 2.11 Implementar testes: model User, login/logout, permissões, validação de senha, soft delete, proteção último admin

## 3. App Teams — Gestão de Times

- [x] 3.1 Implementar models: Team (name unique, description) e TeamMembership (user, team, is_manager)
- [x] 3.2 Implementar validação de pelo menos um gestor por time
- [x] 3.3 Implementar views de CRUD de times — apenas admin: criar, editar, excluir
- [x] 3.4 Implementar views de gestão de membros: adicionar, remover, promover/rebaixar gestor
- [x] 3.5 Implementar listagem de times com filtro por visibilidade (membro vê só seus times, admin vê todos)
- [x] 3.6 Implementar template de detalhe do time com lista de membros e projetos
- [x] 3.7 Implementar testes: models, CRUD, permissões, validação de gestor mínimo, visibilidade

## 4. App Projects — Gestão de Projetos

- [x] 4.1 Implementar model: Project (name, description, status active/archived, FK para Team)
- [x] 4.2 Implementar views de CRUD de projetos — admin e gestores do time: criar, editar, arquivar
- [x] 4.3 Implementar controle de visibilidade: membro vê projetos dos seus times, admin vê todos, 403 para outros
- [x] 4.4 Implementar filtro de projetos arquivados
- [x] 4.5 Implementar confirmação de arquivamento quando há tarefas pendentes (preparar para Milestone 2)
- [x] 4.6 Implementar templates: lista de projetos por time, formulário de criação/edição, detalhe do projeto
- [x] 4.7 Implementar testes: models, CRUD, permissões por papel, visibilidade por time, arquivamento

## 5. Integração e Navegação

- [x] 5.1 Configurar URLs raiz: login como página inicial para não autenticados, redirecionamento pós-login para lista de times
- [x] 5.2 Implementar navbar com links contextuais por papel (admin vê gestão de usuários, todos veem seus times)
- [x] 5.3 Implementar página inicial pós-login (lista de times do usuário)
- [x] 5.4 Implementar mensagens de feedback (success/error) usando Django messages framework
- [x] 5.5 Rodar todos os testes e garantir que passam
