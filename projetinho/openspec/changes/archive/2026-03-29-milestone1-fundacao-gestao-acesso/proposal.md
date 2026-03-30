## Why

A empresa controla projetos e tarefas via Google Sheets, o que causa falta de visibilidade, dados desatualizados e reuniões de status improdutivas. Uma tentativa anterior com Jira falhou por excesso de complexidade. Este milestone estabelece a fundação do sistema — autenticação, times e projetos — priorizando simplicidade radical.

## What Changes

- **Novo projeto Django** com estrutura base, configurações e modelo de usuário customizado (email como login)
- **Sistema de autenticação** com login/logout via email+senha, gestão de sessão (8h de inatividade), e três papéis de acesso (Admin, Gestor, Membro)
- **CRUD de times** com atribuição de membros e gestores, isolamento de visibilidade por time
- **CRUD de projetos** vinculados a times, com status Ativo/Arquivado e controle de acesso por papel
- **Templates Django com Bootstrap** para todas as telas (server-side rendering)
- **Testes automatizados** cobrindo models, views e permissões

## Capabilities

### New Capabilities
- `user-auth`: Cadastro de usuários, login/logout, sessão, papéis de acesso (Admin/Gestor/Membro), soft delete de usuários
- `team-management`: CRUD de times, atribuição de membros e gestores, regras de integridade (mínimo 1 gestor)
- `project-management`: CRUD de projetos por time, status Ativo/Arquivado, controle de visibilidade e permissões

### Modified Capabilities
<!-- Nenhuma — este é o primeiro milestone, não há capabilities existentes -->

## Impact

- **Código**: Projeto Django novo com 3 apps (`accounts`, `teams`, `projects`) + app `core` para templates base
- **Banco de dados**: SQLite com migrations para User customizado, Team, TeamMembership, Project
- **Dependências**: Django, Bootstrap (CDN)
- **Infraestrutura**: Nenhuma — apenas desenvolvimento local neste momento
