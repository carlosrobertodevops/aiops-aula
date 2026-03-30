## ADDED Requirements

### Requirement: Custom User model com email como login
O sistema SHALL usar um modelo de usuário customizado (AbstractUser) com `email` como campo de login (`USERNAME_FIELD`). O campo `email` SHALL ser único e obrigatório. O campo `username` SHALL ser removido do modelo.

#### Scenario: Criar usuário com email válido
- **WHEN** admin cria um usuário com email "joao@empresa.com" e senha "Senha123"
- **THEN** o usuário é criado com email como identificador único

#### Scenario: Rejeitar email duplicado
- **WHEN** admin tenta criar um usuário com email já cadastrado
- **THEN** o sistema retorna erro de validação informando que o email já está em uso

### Requirement: Papéis de acesso
Cada usuário SHALL ter um papel (role) com valor `admin`, `manager` ou `member`. O valor padrão SHALL ser `member`.

#### Scenario: Usuário criado com papel padrão
- **WHEN** admin cria um usuário sem especificar papel
- **THEN** o usuário é criado com papel `member`

#### Scenario: Admin altera papel de usuário
- **WHEN** admin altera o papel de um usuário para `manager`
- **THEN** o papel do usuário é atualizado

### Requirement: Login via email e senha
O sistema SHALL autenticar usuários via email e senha. A mensagem de erro para credenciais inválidas SHALL ser genérica ("Credenciais inválidas"), sem revelar se o email existe ou não.

#### Scenario: Login com credenciais válidas
- **WHEN** usuário submete email e senha corretos
- **THEN** o sistema cria uma sessão e redireciona para a página inicial

#### Scenario: Login com credenciais inválidas
- **WHEN** usuário submete email inexistente ou senha incorreta
- **THEN** o sistema exibe "Credenciais inválidas"

#### Scenario: Login com conta desativada
- **WHEN** usuário desativado tenta fazer login
- **THEN** o sistema exibe "Conta desativada. Contate o administrador."

### Requirement: Gestão de sessão
A sessão SHALL expirar após 8 horas de inatividade. O usuário SHALL poder fazer logout manualmente.

#### Scenario: Sessão expira por inatividade
- **WHEN** o usuário fica inativo por mais de 8 horas
- **THEN** a sessão é encerrada e o usuário é redirecionado para a tela de login

#### Scenario: Logout manual
- **WHEN** o usuário clica em "Sair"
- **THEN** a sessão é encerrada e o usuário é redirecionado para a tela de login

### Requirement: Soft delete de usuários
O admin SHALL poder desativar usuários (soft delete). Usuários desativados SHALL ter `is_active = False` e não SHALL poder fazer login. Os dados do usuário desativado SHALL ser mantidos.

#### Scenario: Admin desativa um usuário
- **WHEN** admin desativa um usuário ativo
- **THEN** o usuário é marcado como inativo e não consegue mais fazer login

#### Scenario: Impedir desativação do último admin
- **WHEN** o último usuário com papel `admin` tenta ser desativado
- **THEN** o sistema bloqueia a ação com mensagem "Não é possível desativar o último administrador"

#### Scenario: Admin reativa um usuário
- **WHEN** admin reativa um usuário desativado
- **THEN** o usuário volta a poder fazer login

### Requirement: Validação de senha
A senha SHALL ter no mínimo 8 caracteres, com pelo menos uma letra e um número.

#### Scenario: Senha válida
- **WHEN** usuário define senha "MinhaSenh4"
- **THEN** a senha é aceita

#### Scenario: Senha sem número
- **WHEN** usuário define senha "SenhaApenas"
- **THEN** o sistema rejeita com mensagem de validação

#### Scenario: Senha muito curta
- **WHEN** usuário define senha "Se1"
- **THEN** o sistema rejeita com mensagem de validação

### Requirement: Admin pode resetar senha de usuário
O admin SHALL poder resetar a senha de qualquer usuário, definindo uma nova senha.

#### Scenario: Reset de senha por admin
- **WHEN** admin define nova senha para um usuário
- **THEN** a senha do usuário é atualizada e ele pode fazer login com a nova senha

### Requirement: Proteção de rotas por autenticação
Todas as páginas do sistema (exceto login) SHALL exigir autenticação. Usuários não autenticados SHALL ser redirecionados para a tela de login.

#### Scenario: Acesso sem autenticação
- **WHEN** usuário não autenticado tenta acessar qualquer página protegida
- **THEN** o sistema redireciona para a tela de login

### Requirement: Gestão de usuários pelo Admin
Apenas usuários com papel `admin` SHALL poder criar, editar, desativar e listar todos os usuários do sistema.

#### Scenario: Admin acessa lista de usuários
- **WHEN** admin acessa a página de gestão de usuários
- **THEN** o sistema exibe todos os usuários cadastrados

#### Scenario: Membro tenta acessar gestão de usuários
- **WHEN** usuário com papel `member` tenta acessar a página de gestão de usuários
- **THEN** o sistema retorna 403 Forbidden
