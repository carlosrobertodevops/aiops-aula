## ADDED Requirements

### Requirement: Modelo de time
Um time SHALL ter nome (único e obrigatório) e descrição (opcional).

#### Scenario: Criar time com nome válido
- **WHEN** admin cria um time com nome "Backend" e descrição "Time de backend"
- **THEN** o time é criado com sucesso

#### Scenario: Rejeitar nome duplicado
- **WHEN** admin tenta criar um time com nome já existente
- **THEN** o sistema retorna erro "Já existe um time com este nome"

### Requirement: Membership de time
Um usuário SHALL poder pertencer a mais de um time. A relação entre usuário e time SHALL ser representada por um modelo intermediário (TeamMembership) com campo `is_manager` (boolean).

#### Scenario: Adicionar membro a um time
- **WHEN** admin adiciona um usuário como membro de um time
- **THEN** o usuário passa a ver os projetos daquele time

#### Scenario: Usuário em múltiplos times
- **WHEN** admin adiciona o mesmo usuário a dois times diferentes
- **THEN** o usuário vê os projetos de ambos os times

### Requirement: Gestores de time
Cada time SHALL ter pelo menos um gestor (membership com `is_manager = True`).

#### Scenario: Promover membro a gestor
- **WHEN** admin marca um membro como gestor do time
- **THEN** o membro passa a ter permissões de gestor naquele time

#### Scenario: Impedir remoção do último gestor
- **WHEN** admin tenta remover o último gestor de um time ou rebaixá-lo a membro
- **THEN** o sistema bloqueia a ação com mensagem "O time precisa ter pelo menos um gestor"

### Requirement: Remoção de membro com tarefas
Quando um membro é removido de um time, as tarefas atribuídas a ele SHALL permanecer atribuídas com indicador visual "Membro removido" para que o gestor reatribua.

#### Scenario: Remover membro com tarefas atribuídas
- **WHEN** admin remove um membro que tem tarefas atribuídas em projetos do time
- **THEN** o membro é removido do time e as tarefas mantêm a atribuição com indicador "Membro removido"

#### Scenario: Remover membro sem tarefas
- **WHEN** admin remove um membro sem tarefas atribuídas
- **THEN** o membro é removido do time sem efeitos colaterais

### Requirement: Permissões de gestão de times
Apenas usuários com papel `admin` SHALL poder criar, editar e excluir times, e gerenciar membros.

#### Scenario: Admin cria um time
- **WHEN** admin acessa a página de criação de times
- **THEN** o formulário é exibido e o time pode ser criado

#### Scenario: Membro tenta criar time
- **WHEN** usuário com papel `member` tenta acessar a criação de times
- **THEN** o sistema retorna 403 Forbidden

#### Scenario: Gestor tenta criar time
- **WHEN** usuário com papel `manager` tenta acessar a criação de times
- **THEN** o sistema retorna 403 Forbidden

### Requirement: Visualização de times
Cada usuário SHALL ver apenas os times dos quais é membro. Admins SHALL ver todos os times.

#### Scenario: Membro vê seus times
- **WHEN** membro acessa a lista de times
- **THEN** o sistema exibe apenas os times dos quais ele é membro

#### Scenario: Admin vê todos os times
- **WHEN** admin acessa a lista de times
- **THEN** o sistema exibe todos os times cadastrados
