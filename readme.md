# Sistema de Controle de Visitantes

Sistema web para gerenciamento de visitantes, veículos e autorizações de acesso, desenvolvido em Python com FastAPI e PostgreSQL.

O sistema permite controlar todo o ciclo de vida das autorizações de acesso, desde sua emissão até o acompanhamento do histórico, além de possibilitar importações em lote de visitantes e autorizações.

As autorizações podem ser exportadas em forma de QR CODE e validadas por WEBCAM ligada à estação, tablet ou smartphone no(s) qual(is) opera(m) o sistema.

---

# Principais funcionalidades

## Autenticação

- Login por usuário e senha.
- Controle de sessões.
- Expiração automática de sessões.
- Controle de usuários ativos e inativos.
- Autenticação via Bearer Token.
- Verificação de visitantes por leitura de QR code.

---

## Usuários

- Cadastro de usuários.
- Alteração de usuários.
- Exclusão de usuários.
- Controle de credenciais.
- Associação do usuário a um setor.
- Associação indireta ao local por meio do setor.

---

## Credenciais

Gerenciamento das credenciais de acesso ao sistema.

Exemplos:

- Administrador
- Recepção
- Segurança

Cada credencial determina quais funcionalidades o usuário poderá acessar.

---

## Locais

Cadastro dos locais existentes.

Exemplos:

- Matriz
- Filial Norte
- Unidade Industrial

Cada setor pertence a um local.

---

## Setores

Cadastro dos setores existentes.

Exemplos:

- RH
- Financeiro
- Almoxarifado
- TI

Cada usuário pertence a um setor.

As autorizações também ficam associadas ao setor solicitante.

---

## Empresas

Cadastro das empresas autorizadas.

Cada visitante pertence a uma empresa.

Durante a importação em lote:

- empresas existentes são reutilizadas;
- empresas inexistentes são criadas automaticamente.

---

## Visitantes

Cadastro completo dos visitantes.

Informações armazenadas:

- Nome
- CPF
- RG
- E-mail
- Celular
- Empresa

O sistema evita duplicidade utilizando o CPF como identificador.

Durante a importação em lote:

- visitantes existentes são reutilizados;
- visitantes inexistentes são criados automaticamente.

---

## Veículos

Cadastro de veículos.

Informações armazenadas:

- Placa
- Marca
- Modelo/Tipo
- Cor
- Observações

Durante a importação em lote:

- caso a placa já exista, o veículo é reutilizado;
- caso não exista, é criado automaticamente;
- caso a placa esteja vazia, o visitante não será associado a nenhum veículo.

---

## Autorizações

Emissão de autorizações individuais.

Cada autorização possui:

- Visitante
- Veículo (opcional)
- Setor solicitante
- Período de validade
- Status

---

## Consulta de autorizações

Consulta completa das autorizações cadastradas.

Permite visualizar:

- visitante;
- empresa;
- veículo;
- período;
- status;
- solicitante;
- histórico.

---

## Alteração de autorizações

Permite alterar:

- período;
- status;
- veículo;
- visitante.

As alterações ficam registradas no histórico.

---

## Exclusão de autorizações

Permite remover autorizações.

A exclusão também gera registro no histórico.

---

## Histórico

Cada autorização possui histórico próprio.

São registrados eventos como:

- autorização criada;
- autorização criada por importação em lote;
- alteração de status;
- alteração de período;
- exclusão.

Cada registro informa:

- usuário responsável;
- descrição da alteração;
- data e hora.

---

# Importação em lote

O sistema suporta importação por planilhas.

Formatos aceitos:

- CSV
- XLSX
- ODS

---

## Campos importados

A planilha contém apenas:

| Campo | Obrigatório |
|--------|-------------|
| CPF | Sim |
| Nome | Sim |
| Empresa | Sim |
| Placa | Não |
| De | Sim |
| Até | Sim |

---

## Validação

Antes da gravação, todas as linhas são validadas.

São verificados, entre outros:

- CPF
- Nome
- Empresa
- Datas
- Período

Nenhuma informação é gravada nesta etapa.

---

## Revisão

Após a validação é exibida uma tabela de revisão.

Cada linha apresenta:

- dados importados;
- resultado da validação.

Linhas válidas aparecem como:

```
✔ OK
```

Linhas inválidas apresentam:

```
❌ X erros
```

Ao posicionar o mouse sobre o resultado são exibidas todas as mensagens de erro.

---

## Correção direta

Campos inválidos aparecem destacados.

Ao clicar em um campo com erro é possível corrigi-lo imediatamente.

Após a edição:

- a linha é reenviada ao servidor;
- a validação é executada novamente;
- o resultado é atualizado sem necessidade de reenviar toda a planilha.

Campos corrigidos passam a ser destacados em verde.

---

## Linhas vazias

Linhas completamente vazias são ignoradas durante a importação.

Não aparecem na tela de revisão.

---

## Empresas

Durante a confirmação da importação:

- empresas existentes são reutilizadas;
- empresas inexistentes são criadas automaticamente.

---

## Visitantes

Durante a confirmação:

- visitantes são identificados pelo CPF;
- caso já existam, são reutilizados;
- caso contrário, são cadastrados automaticamente.

---

## Veículos

A importação considera apenas a placa.

Se:

- a placa existir, o veículo é reutilizado;
- a placa não existir, o veículo é criado;
- a placa estiver vazia, nenhuma associação é realizada.

---

## Persistência

A confirmação executa toda a importação em uma única transação.

Isso significa que:

- todas as autorizações são gravadas;
- ou nenhuma delas é gravada.

Não existem importações parcialmente concluídas.

---

## Histórico

Cada autorização importada gera automaticamente um histórico específico de criação por lote.

---

# Parâmetros do sistema

Algumas regras são configuráveis através da tabela de parâmetros do sistema.

Exemplo:

- status inicial das autorizações importadas.

Isso permite alterar regras sem necessidade de modificar o código-fonte.

---

# Tecnologias utilizadas

- Python
- FastAPI
- PostgreSQL
- HTML
- CSS
- JavaScript

---

# Estrutura do projeto

```
database/
security/
controllers/
models/
repositories/
schemas/
services/
static/
templates/
utils/
config/
tests/
docs/
```

Cada camada possui uma responsabilidade específica.

### Database

Possui o .SQL utilizado para criar o MER empregado pelo sistema em base de dados do tipo Postgres.

### Security

Gerencia tokens e permissões concedidas aos diferentes tipos de usuários do sistema.

### Controllers

Recebem requisições HTTP.

### Services

Implementam as regras de negócio.

### Repositories

Realizam acesso ao banco de dados.

### Models

Representam os objetos internos da aplicação.

### Schemas

Representam estruturas utilizadas para comunicação entre cliente e servidor.

### Utils

Funções auxiliares.

### Static

Arquivos JavaScript, CSS e imagens.

### Templates

Páginas HTML.

### Tests

Testes para verificar as funcionalidades do sistema.

### Docs

Documentações suplementares do projeto.

---

# Arquitetura

O projeto segue uma arquitetura em camadas.

```
Frontend

↓

Controller

↓

Service

↓

Repository

↓

PostgreSQL
```

Essa separação reduz o acoplamento e facilita manutenção e testes.

---

# Como executar

## Requisitos

- Python 3.10+
- PostgreSQL

## Instalação

Instale as dependências:

```bash
pip install -r requirements.txt
```

Setar as variáveis locais necessárias:

```bash
export DB_HOST_SISVISITANTES=<HOST DO BANCO DE DADOS>
export DB_PORT_SISVISITANTES=<PORTA DO BANCO DE DADOS>
export DB_NAME_SISVISITANTES=<NOME DO BANCO DE DADOS>
export DB_USER_SISVISITANTES=<USER DO BANCO DE DADOS>
export DB_PASSWORD_SISVISITANTES=<SENHA DO BANCO DE DADOS>
```

Se necessário, também é preciso setar o segredo do sistema leitor de QRCODE.

```bash
export QR_CODE_SECRET=<SENHA_QR_CODE>
```

Execute:

```bash
uvicorn app:app --reload
```

A aplicação ficará disponível em:

```
http://localhost:8000
```

---

# Organização do código

O projeto procura seguir os seguintes princípios:

- responsabilidade única por classe;
- separação entre regras de negócio e persistência;
- reutilização de serviços;
- transações explícitas;
- código organizado em camadas;
- baixa duplicação de lógica.

---

# API

O projeto conta com API próprio para facilitar a integração a outros sistemas. Acessar url /docs para verificar Swagger da API desenvolvida (conforme disponibilizado pela biblioteca FastAPI).

# Licença

Projeto desenvolvido pelo CT(EN) Guilherme VIEIRA DANTAS
