## ADDED Requirements

### Requirement: Modelo de projeto
Um projeto SHALL ter nome (obrigatório), descrição (opcional) e status (`active` ou `archived`, padrão `active`). Um projeto SHALL pertencer a exatamente um time.

#### Scenario: Criar projeto em um time
- **WHEN** gestor cria um projeto "API v2" no time "Backend"
- **THEN** o projeto é criado com status `active` vinculado ao time

#### Scenario: Projeto pertence a um único time
- **WHEN** um projeto é criado
- **THEN** ele está vinculado a exatamente um time (ForeignKey)

### Requirement: Arquivamento de projetos
Projetos SHALL poder ser arquivados. Projetos arquivados SHALL sair da visualização padrão mas SHALL poder ser consultados via filtro.

#### Scenario: Arquivar projeto sem tarefas pendentes
- **WHEN** gestor arquiva um projeto sem tarefas em andamento
- **THEN** o projeto é marcado como `archived` e não aparece mais na listagem padrão

#### Scenario: Arquivar projeto com tarefas em andamento
- **WHEN** gestor arquiva um projeto que tem tarefas não concluídas
- **THEN** o sistema exibe confirmação "Este projeto tem X tarefas não concluídas. Deseja arquivar mesmo assim?" e permite prosseguir

#### Scenario: Filtrar projetos arquivados
- **WHEN** usuário ativa o filtro de projetos arquivados
- **THEN** o sistema exibe os projetos arquivados do time

### Requirement: Permissões de gestão de projetos
Apenas Admin e Gestores do time SHALL poder criar, editar e arquivar projetos dentro do time.

#### Scenario: Gestor cria projeto no seu time
- **WHEN** gestor de um time acessa a criação de projeto naquele time
- **THEN** o formulário é exibido e o projeto pode ser criado

#### Scenario: Gestor tenta criar projeto em outro time
- **WHEN** gestor tenta criar projeto em um time que não gerencia
- **THEN** o sistema retorna 403 Forbidden

#### Scenario: Membro tenta criar projeto
- **WHEN** membro tenta criar um projeto
- **THEN** o sistema retorna 403 Forbidden

#### Scenario: Admin cria projeto em qualquer time
- **WHEN** admin cria projeto em qualquer time
- **THEN** o projeto é criado com sucesso

### Requirement: Visibilidade de projetos por time
Membros de um time SHALL ver todos os projetos ativos daquele time. Usuários fora do time SHALL NOT ver os projetos (exceto Admin, que vê tudo).

#### Scenario: Membro vê projetos do seu time
- **WHEN** membro acessa a lista de projetos
- **THEN** o sistema exibe os projetos ativos dos times dos quais é membro

#### Scenario: Membro não vê projetos de outro time
- **WHEN** membro tenta acessar um projeto de um time do qual não é membro
- **THEN** o sistema retorna 403 Forbidden

#### Scenario: Admin vê projetos de qualquer time
- **WHEN** admin acessa projetos de qualquer time
- **THEN** o sistema exibe os projetos normalmente

### Requirement: Listagem de projetos dentro do time
A visualização de projetos SHALL ser organizada por time. Ao acessar um time, o usuário SHALL ver a lista de projetos ativos daquele time.

#### Scenario: Visualizar projetos de um time
- **WHEN** membro acessa a página de um time do qual é membro
- **THEN** o sistema exibe a lista de projetos ativos daquele time

#### Scenario: Time sem projetos
- **WHEN** membro acessa um time que não tem projetos
- **THEN** o sistema exibe mensagem "Nenhum projeto neste time"
