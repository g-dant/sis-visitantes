# Sistema de Controle de Visitantes

Sistema web para gerenciamento de visitantes, veículos, empresas e autorizações de acesso.

O sistema permite cadastrar e administrar visitantes, empresas, veículos, usuários, credenciais, permissões, setores e locais, além de emitir, consultar, alterar e revogar autorizações de acesso.

Também possui um mecanismo de importação em lote de autorizações por planilha, com normalização, validação, pré-visualização, identificação de inconsistências e verificação de colisão de períodos.

## OBSERVAÇÃO

Este documento possui natureza técnica. Para consultar o manual de utilização do usuário, acesse [[https://github.com/g-dant/sis-visitantes/src/branch/main/manual-usuario.md]]

---

# 1. Visão geral

O sistema tem como objetivo central controlar autorizações de acesso de visitantes.

Uma autorização relaciona:

- um visitante;
- uma empresa;
- um período de validade;
- um setor solicitante;
- opcionalmente, um veículo;
- um status de autorização;
- o histórico das operações realizadas.

O visitante é identificado principalmente pelo CPF.

O sistema mantém o cadastro do visitante separado do cadastro da autorização. Dessa forma, um visitante pode possuir várias autorizações ao longo do tempo.

A empresa também possui uma entidade própria e a autorização mantém sua própria referência à empresa.

---

# 2. Principais funcionalidades

## 2.1. Usuários

Permite:

- cadastrar usuários;
- editar usuários;
- ativar ou desativar usuários;
- consultar usuários;
- associar usuário a um tipo;
- associar usuário a um setor;
- associar usuário a uma credencial;
- definir senha;
- registrar data de criação;
- registrar data da última alteração.

Cada usuário possui:

- nome;
- e-mail;
- telefone;
- tipo de usuário;
- setor;
- credencial;
- senha armazenada como hash;
- indicador de ativo;
- data de criação;
- data da última alteração.

O e-mail do usuário é único.

---

# 3. Autenticação e autorização

O sistema utiliza autenticação baseada em sessão/token.

As sessões são armazenadas no banco de dados e possuem:

- usuário;
- token;
- data de início;
- data de expiração.

O acesso às funcionalidades é controlado por permissões.

A estrutura de autorização possui:

```text
Usuário
   |
   +-- Tipo de usuário
   |
   +-- Setor
   |
   +-- Credencial
           |
           +-- Permissões
```

Uma credencial pode possuir diversas permissões.

Uma permissão possui:

- código;
- descrição.

As permissões são utilizadas pelos endpoints para controlar as operações permitidas.

---

# 4. Estrutura organizacional

O sistema possui as seguintes entidades organizacionais.

## Local

Representa um local físico ou unidade.

Campos principais:

- código;
- descrição;
- ativo.

O código é único.

## Setor

Representa um setor pertencente a um local.

Campos principais:

- código;
- descrição;
- ativo;
- local.

O código do setor é único.

## Tipo de usuário

Representa o tipo funcional do usuário.

Campos:

- nome;
- ativo.

O nome é único.

## Credencial

Representa um conjunto de permissões.

Campos:

- nome;
- ativo.

O nome é único.

## Permissão

Representa uma capacidade do sistema.

Campos:

- código;
- descrição.

O código é único.

---

# 5. Empresas

A entidade `empresa` representa a empresa associada ao visitante e às autorizações.

Campos principais:

- nome;
- CNPJ;
- ativo.

O nome da empresa é único.

Os dados de empresa são normalizados para maiúsculas no banco.

---

# 6. Visitantes

A entidade `visitante` representa a pessoa que receberá autorização de acesso.

Campos:

- nome;
- e-mail;
- celular;
- RG;
- CPF;
- empresa;
- ativo.

O CPF é único no banco.

O CPF é o principal identificador utilizado para localizar um visitante.

Os dados cadastrais do visitante são normalizados para maiúsculas no banco.

---

# 7. Veículos

Um visitante pode utilizar um veículo durante uma autorização.

A entidade `veiculo` possui:

- placa;
- cor;
- marca;
- tipo;
- observações;
- ativo.

A placa é única.

A placa pode ser associada a diferentes visitantes através da tabela de relacionamento `visitante_veiculo`.

Durante a importação:

- se a placa estiver vazia, a autorização é criada sem veículo;
- se a placa já existir, o veículo existente é reutilizado;
- se a placa não existir, o veículo é criado.

---

# 8. Autorizações

A autorização é a principal entidade operacional do sistema.

Uma autorização possui:

- visitante;
- empresa;
- status;
- primeiro dia;
- último dia;
- setor solicitante;
- veículo opcional.

A estrutura simplificada é:

```text
Autorização
 |
 +-- Visitante
 |     |
 |     +-- CPF
 |     +-- Nome
 |     +-- Empresa cadastrada
 |
 +-- Empresa da autorização
 |
 +-- Status
 |
 +-- Período
 |     |
 |     +-- Primeiro dia
 |     +-- Último dia
 |
 +-- Setor solicitante
 |
 +-- Veículo
```

A empresa do visitante e a empresa da autorização são referências distintas.

---

# 9. Histórico das autorizações

As operações relevantes sobre uma autorização são registradas na tabela `historico_autorizacao`.

Cada registro contém:

- autorização;
- usuário responsável;
- data e hora;
- descrição da operação.

O histórico é utilizado para registrar operações como:

- criação;
- alteração de período;
- alteração de status;
- exclusão.

As operações de alteração de autorização registram o usuário responsável.

---

# 10. Status das autorizações

O sistema possui uma distinção importante entre:

1. **status armazenado da autorização**;
2. **status de exibição da autorização**.

O status armazenado é o status efetivamente gravado na tabela `autorizacao`.

O status de exibição é calculado pela view `autorizacao_consulta`.

Portanto, nem todo estado apresentado ao usuário corresponde a um registro independente na tabela `status_autorizacao`.

---

# 11. Status armazenado

Cada autorização possui:

```text
id_status_autorizacao
```

Esse campo referencia a tabela:

```text
status_autorizacao
```

Um status possui:

- nome;
- descrição;
- ativo;
- participa_colisao.

O campo `participa_colisao` é especialmente importante para a regra de conflito de períodos.

---

# 12. Status de exibição

O sistema calcula `status_exibicao` a partir do status armazenado e das datas da autorização.

A regra atualmente implementada é:

```text
                         status armazenado = "Autorizada"
                                  |
                 +----------------+----------------+
                 |                |                |
        primeiro_dia > hoje   ultimo_dia < hoje    caso contrário
                 |                |                |
                 v                v                v
             Pendente          Expirada         Autorizada
```

## 12.1. Autorizada

A autorização possui status armazenado `Autorizada`.

Se:

```text
primeiro_dia <= hoje <= ultimo_dia
```

o status de exibição permanece:

```text
Autorizada
```

Representa uma autorização cujo período está vigente.

## 12.2. Pendente

Uma autorização cujo status armazenado é `Autorizada` é exibida como:

```text
Pendente
```

quando:

```text
primeiro_dia > hoje
```

Isso significa que a autorização já foi emitida, mas seu período de validade ainda não começou.

`Pendente` é, portanto, um **estado derivado**.

Não é necessário que exista um registro independente chamado `Pendente` na tabela de status para que uma autorização apareça dessa maneira.

## 12.3. Expirada

Uma autorização cujo status armazenado é `Autorizada` é exibida como:

```text
Expirada
```

quando:

```text
ultimo_dia < hoje
```

Isso significa que o período de validade já terminou.

`Expirada` também é um **estado derivado**.

Não representa necessariamente uma alteração do `id_status_autorizacao` para um status chamado `Expirada`.

## 12.4. Outros status

Quando o status armazenado não é `Autorizada`, o sistema utiliza o próprio nome do status como `status_exibicao`.

Assim:

```text
status armazenado = X
status de exibição = X
```

Por exemplo, se existir um status armazenado chamado `Revogada`, a autorização será exibida como:

```text
Revogada
```

---

# 13. Relação entre os estados

É importante não interpretar `Pendente`, `Autorizada` e `Expirada` como três estados persistidos equivalentes.

A relação é:

```text
Status armazenado
        |
        |-- Autorizada
        |      |
        |      +-- período ainda não começou --> Pendente
        |      |
        |      +-- período vigente ------------> Autorizada
        |      |
        |      +-- período terminou ------------> Expirada
        |
        +-- qualquer outro status -------------> próprio nome
```

| Status armazenado | Condição | Status exibido |
|---|---|---|
| Autorizada | `primeiro_dia > hoje` | Pendente |
| Autorizada | `primeiro_dia <= hoje <= ultimo_dia` | Autorizada |
| Autorizada | `ultimo_dia < hoje` | Expirada |
| Qualquer outro | qualquer condição | Nome do próprio status |

---

# 14. Revogação

A revogação de uma autorização é realizada por alteração de status.

O sistema não utiliza a exclusão física da autorização como mecanismo normal de revogação.

Assim, uma autorização revogada continua existindo no banco e pode permanecer disponível para consulta e histórico.

A alteração de status também é registrada no histórico da autorização.

A exclusão física é uma operação distinta e não deve ser confundida com revogação.

---

# 15. Regra de colisão de períodos

A colisão de períodos é uma das principais regras de negócio do sistema.

O objetivo é impedir que o mesmo visitante possua autorizações, dentro de determinados status, com períodos de validade sobrepostos.

A verificação é baseada no:

- CPF do visitante;
- primeiro dia;
- último dia;
- status da autorização existente.

A empresa e o veículo **não fazem parte da chave de colisão**.

---

# 16. Regra matemática da colisão

Considere uma autorização existente:

```text
[E1, E2]
```

e uma nova autorização:

```text
[N1, N2]
```

Existe colisão quando:

```text
E1 <= N2
e
E2 >= N1
```

ou, equivalentemente:

```text
N1 <= E2
e
N2 >= E1
```

Os intervalos são inclusivos.

Portanto, se uma autorização termina no mesmo dia em que outra começa, os períodos são considerados conflitantes.

### Exemplos

#### Sem colisão

```text
Existente: 01/01/2026 ───── 10/01/2026
Nova:                         11/01/2026 ───── 20/01/2026
```

Não há sobreposição.

#### Com colisão

```text
Existente: 01/01/2026 ───────────── 10/01/2026
Nova:                         10/01/2026 ───── 20/01/2026
                              ^
                           colisão
```

O dia 10 pertence aos dois intervalos.

#### Com colisão parcial

```text
Existente: 01/01/2026 ─────────────── 20/01/2026
Nova:                   10/01/2026 ───────────── 30/01/2026
```

Há sobreposição.

#### Nova autorização completamente dentro da existente

```text
Existente: 01/01/2026 ───────────────────────── 30/01/2026
Nova:             10/01/2026 ─────── 20/01/2026
```

Há colisão.

#### Existente completamente dentro da nova

```text
Nova:       01/01/2026 ───────────────────────────── 30/01/2026
Existente:             10/01/2026 ─────── 20/01/2026
```

Há colisão.

---

# 17. Quem pode colidir?

A colisão é determinada pelo visitante.

O visitante é identificado pelo CPF.

Portanto:

```text
mesmo CPF + períodos sobrepostos = possível colisão
```

Enquanto:

```text
CPFs diferentes + períodos sobrepostos = não há colisão entre os visitantes
```

A empresa não altera essa regra.

Exemplo:

```text
CPF 111
Empresa A
01/08 ─── 10/08

CPF 111
Empresa B
05/08 ─── 15/08
```

Existe colisão.

Já:

```text
CPF 111
Empresa A
01/08 ─── 10/08

CPF 222
Empresa A
05/08 ─── 15/08
```

não existe colisão entre as autorizações.

---

# 18. Participação do status na colisão

Cada status possui o campo:

```text
participa_colisao
```

Esse campo determina se uma autorização naquele status deve ser considerada na verificação de conflitos.

A regra é:

```text
participa_colisao = true
```

A autorização participa da verificação.

```text
participa_colisao = false
```

A autorização não participa da verificação.

Portanto, não basta verificar se existe uma autorização do mesmo visitante no período.

Também é necessário verificar se o status dessa autorização participa de colisão.

---

# 19. Consulta de colisão

A consulta de colisão verifica:

```text
visitante.CPF = CPF informado
```

e:

```text
status_autorizacao.participa_colisao = true
```

e:

```text
autorizacao.primeiro_dia <= novo_ultimo_dia
```

e:

```text
autorizacao.ultimo_dia >= novo_primeiro_dia
```

Na edição de uma autorização, a própria autorização que está sendo editada é ignorada na busca.

Isso evita que uma autorização colida consigo mesma.

---

# 20. Colisão durante a importação

A importação em lote realiza a verificação de colisão contra autorizações já existentes no banco.

Para cada linha válida da planilha, o sistema consulta:

```text
CPF
+
Primeiro Dia
+
Último Dia
```

A consulta procura uma autorização do mesmo visitante cujo status tenha:

```text
participa_colisao = true
```

e cujo período se sobreponha ao período da planilha.

Se uma autorização conflitante for encontrada:

```text
linha.valida = false
```

e:

```text
linha.colisao_intervalo = true
```

A importação também registra um erro global indicando que existem visitantes com autorizações que colidem com períodos já cadastrados.

---

# 21. Importante: colisão é verificada contra o banco

A verificação implementada durante a validação da planilha procura colisões nas autorizações já existentes no banco de dados.

A regra de coerência da própria planilha é tratada separadamente.

Portanto, existem dois mecanismos diferentes:

```text
                 PLANILHA
                    |
          +---------+---------+
          |                   |
          v                   v
   Coerência interna    Colisão com banco
          |                   |
          |                   |
     mesmo CPF           mesmo CPF
     deve ter            + período
     mesmo nome          sobreposto
     e empresa           + status que
                         participa
                         de colisão
```

---

# 22. Coerência interna da planilha

A própria planilha precisa ser coerente.

Para cada CPF, o sistema constrói conjuntos de:

- nomes;
- empresas.

Os valores são comparados após normalização em maiúsculas.

## 22.1. Mesmo CPF com nomes diferentes

Exemplo:

```text
CPF      Nome
111      João Silva
111      João Souza
```

Resultado:

```text
ERRO
```

Todas as linhas daquele CPF são marcadas como inválidas.

## 22.2. Mesmo CPF com empresas diferentes

Exemplo:

```text
CPF      Empresa
111      Empresa A
111      Empresa B
```

Resultado:

```text
ERRO
```

Todas as linhas daquele CPF são marcadas como inválidas.

## 22.3. Mesmo CPF com mesmo nome e mesma empresa

Exemplo:

```text
CPF      Nome          Empresa
111      João Silva    Empresa A
111      João Silva    Empresa A
```

Resultado:

```text
OK
```

As linhas podem representar autorizações diferentes, desde que não violem as demais regras, especialmente a de colisão com autorizações existentes.

---

# 23. Diferença entre divergência na planilha e divergência no banco

Existem duas situações distintas.

## Divergência dentro da planilha

É uma inconsistência bloqueante.

Exemplo:

```text
CPF 111
João Silva
Empresa A

CPF 111
João Souza
Empresa A
```

Resultado:

```text
ERRO
```

## Divergência em relação ao cadastro existente

É um aviso não bloqueante.

Exemplo:

```text
Banco:
CPF 111 -> João Silva

Planilha:
CPF 111 -> João Souza
```

Resultado:

```text
AVISO: Nome divergente.
```

A linha continua podendo ser importada.

O nome cadastrado no banco não é automaticamente substituído pelo nome da planilha.

---

# 24. Empresa durante a importação

Durante a persistência da importação, a empresa da linha é:

1. localizada pelo nome;
2. criada caso ainda não exista;
3. utilizada na autorização;
4. utilizada para atualizar a empresa associada ao visitante existente.

Portanto, se o CPF já existir no banco, o visitante é reutilizado.

A empresa do visitante é atualizada para a empresa informada na importação.

Isso é diferente da divergência de nome:

```text
Nome divergente:
    aviso
    não altera nome do visitante

Empresa diferente:
    visitante existente é reutilizado
    empresa do visitante é atualizada
```

A autorização criada também recebe a empresa correspondente à linha importada.

---

# 25. Importação em lote

A importação possui as seguintes etapas:

```text
Arquivo
   |
   v
Leitura da planilha (em CSV, XLSX ou ODS)
   |
   v
Normalização
   |
   v
Validação individual das linhas
   |
   v
Verificação de colisões
   |
   v
Verificação de coerência da planilha
   |
   v
Pré-visualização
   |
   v
Correção manual, se necessário
   |
   v
Revalidação
   |
   v
Confirmação
   |
   v
Persistência em transação
```

---

# 26. Campos da importação

Os dados utilizados pela importação incluem:

| Campo | Descrição |
|---|---|
| CPF | Identificação do visitante |
| Nome | Nome do visitante |
| Empresa | Empresa do visitante/autorização |
| Placa | Placa do veículo |
| Primeiro Dia | Início da autorização |
| Último Dia | Fim da autorização |

---

# 27. Normalização da planilha

Durante a leitura da planilha:

- `CPF` é lido da coluna correspondente;
- `Nome` é lido da coluna correspondente;
- `Empresa` é lido da coluna correspondente;
- `Placa` é lido da coluna correspondente;
- `Primeiro Dia` pode ser obtido da coluna `Primeiro Dia` ou `De`;
- `Último Dia` pode ser obtido da coluna `Último Dia` ou `Até`.

Linhas completamente vazias são ignoradas.

---

# 28. Validação básica da importação

Cada linha é validada individualmente.

São verificadas, entre outras, as seguintes condições.

## CPF

O CPF:

- deve estar informado;
- é normalizado para conter somente os dígitos;
- deve ser válido.

## Nome

O nome deve estar informado.

## Datas

Devem existir:

- primeiro dia;
- último dia.

## Placa

A placa é opcional.

Quando não informada, é convertida para uma string vazia para representar ausência de veículo.

---

# 29. Resultado da validação

Cada linha possui:

```text
valida
```

que indica se pode ser importada.

Também pode possuir:

```text
erros
```

e:

```text
avisos
```

A diferença é importante:

### Erro

Impede a importação da linha.

### Aviso

Não impede a importação.

Uma linha também pode possuir informações auxiliares para a interface de pré-visualização, como:

- `alterada`;
- `campos_alterados`;
- `colisao_intervalo`;
- `nome_divergente`;
- `empresa_divergente`;
- `nome_cadastrado`;
- `nome_planilha`;
- `nome_banco_divergente`.

---

# 30. Revalidação

Após a pré-visualização, o usuário pode corrigir valores.

O sistema permite:

- revalidar uma linha;
- revalidar a planilha inteira;
- confirmar a importação.

A finalidade é permitir que erros detectados durante a pré-visualização sejam corrigidos antes da persistência.

---

# 31. Persistência da importação

A persistência ocorre dentro de uma transação.

Para cada linha:

1. a empresa é localizada ou criada;
2. o visitante é localizado pelo CPF ou criado;
3. o veículo é localizado ou criado;
4. a autorização é criada;
5. o histórico de criação da autorização é registrado.

Ao final:

```text
COMMIT
```

Se ocorrer uma exceção:

```text
ROLLBACK
```

Assim, a operação de importação não deve deixar parcialmente persistido um lote que falhou durante a gravação.

---

# 32. Status padrão da importação

As autorizações criadas pela importação utilizam o parâmetro:

```text
STATUS_AUTORIZACAO_LOTE_PADRAO
```

Esse parâmetro define o status armazenado inicialmente nas autorizações criadas pelo lote.

O sistema não fixa diretamente o ID do status no código da persistência; ele consulta o parâmetro do sistema.

---

# 33. Parâmetros do sistema

A tabela `parametro_sistema` permite armazenar configurações em formato:

```text
chave -> valor
```

Exemplos de utilização:

```text
STATUS_AUTORIZACAO_LOTE_PADRAO
```

O serviço fornece operações para:

- listar parâmetros;
- buscar por ID;
- buscar por chave;
- criar;
- atualizar;
- excluir;
- obter valor como string;
- obter valor como inteiro;
- obter valor como booleano.

---

# 34. Consulta de autorizações

A view:

```text
autorizacao_consulta
```

consolida informações necessárias para apresentação das autorizações.

Ela reúne:

- visitante;
- CPF;
- RG;
- e-mail;
- celular;
- empresa;
- status armazenado;
- status de exibição;
- setor;
- solicitante;
- veículo;
- período.

O `status_exibicao` é calculado nessa view.

---

# 35. Painel de autorizações

A view:

```text
painel_autorizacao
```

agrupa as autorizações pelo:

```text
status_exibicao
```

e retorna a quantidade de autorizações em cada estado de exibição.

---

# 36. Endpoints principais

O módulo de autorizações possui, entre outras, as seguintes operações:

```text
GET    /autorizacoes
GET    /autorizacoes/{id_autorizacao}

POST   /autorizacoes
PUT    /autorizacoes/{id_autorizacao}

PATCH  /autorizacoes/{id_autorizacao}/status

DELETE /autorizacoes/{id_autorizacao}

GET    /autorizacoes-consulta/status-exibicao

GET    /autorizacoes/importacao/modelo
POST   /autorizacoes/importar

POST   /importacao/revalidar-linha
POST   /importacao/revalidar-planilha
POST   /importacao/confirmar
```

Os endpoints são protegidos por permissões específicas.

---

# 37. Permissões de autorização

As operações de autorização utilizam permissões específicas, como:

```text
AUTORIZACAO_VISUALIZAR
AUTORIZACAO_CRIAR
AUTORIZACAO_EDITAR
AUTORIZACAO_ALTERAR_STATUS
AUTORIZACAO_EXCLUIR
AUTORIZACAO_IMPORTAR
```

O controle efetivo é realizado pelo mecanismo de permissões do sistema.

---

# 38. Banco de dados

O projeto utiliza PostgreSQL.

Principais tabelas:

```text
credencial
credencial_permissao
empresa
local
parametro_sistema
permissao
status_autorizacao
tipo_usuario
veiculo
setor
usuario
visitante
visitante_veiculo
autorizacao
historico_autorizacao
sessao
```

Principais relacionamentos:

```text
local
  |
  +-- setor
        |
        +-- usuario

tipo_usuario
  |
  +-- usuario

credencial
  |
  +-- credencial_permissao
        |
        +-- permissao

empresa
  |
  +-- visitante
  |
  +-- autorizacao

visitante
  |
  +-- visitante_veiculo
  |
  +-- autorizacao

veiculo
  |
  +-- visitante_veiculo
  |
  +-- autorizacao

autorizacao
  |
  +-- historico_autorizacao
```

---

# 39. Integridade do banco

O banco possui chaves primárias, estrangeiras e restrições de unicidade.

Exemplos:

- CPF de visitante é único;
- placa de veículo é única;
- nome de empresa é único;
- código de setor é único;
- código de permissão é único;
- e-mail de usuário é único;
- nome de credencial é único;
- nome de status é único.

As chaves estrangeiras garantem a integridade dos relacionamentos.

O banco não utiliza `CASCADE` por padrão nas relações principais.

---

# 40. Normalização de dados

Existem triggers no PostgreSQL para normalizar determinados campos para maiúsculas.

## Empresa

São convertidos para maiúsculas:

- nome;
- CNPJ.

## Veículo

São convertidos para maiúsculas:

- placa;
- cor;
- marca;
- tipo;
- observações.

## Visitante

São convertidos para maiúsculas:

- nome;
- e-mail;
- celular;
- RG;
- CPF.

A finalidade é manter os dados padronizados no banco.

---

# 41. Arquitetura

O backend segue uma separação por camadas.

Estrutura conceitual:

```text
Controller
    |
    v
Service
    |
    v
Repository
    |
    v
PostgreSQL
```

## Controllers

Responsáveis por:

- receber requisições HTTP;
- validar entrada através dos modelos;
- controlar autenticação/permissão;
- chamar os serviços;
- retornar respostas HTTP.

## Services

Responsáveis pelas regras de negócio.

Exemplos:

```text
AutorizacaoService
VisitanteService
EmpresaService
VeiculoService
StatusAutorizacaoService
ParametroSistemaService
```

A importação possui serviços específicos para:

```text
normalização
validação
persistência
```

## Repositories

Responsáveis pelo acesso ao banco de dados.

Exemplos:

```text
AutorizacaoRepository
VisitanteRepository
EmpresaRepository
VeiculoRepository
StatusAutorizacaoRepository
ParametroSistemaRepository
```

---

# 42. Importação — separação de responsabilidades

A importação é dividida em etapas específicas.

## Normalização

Responsável por transformar os dados da planilha em objetos internos.

```text
NormalizadorImportacaoService
```

## Validação

Responsável por:

- validar CPF;
- validar nome;
- validar datas;
- validar placa;
- verificar nome divergente no banco;
- verificar colisões;
- verificar coerência entre linhas.

```text
ValidacaoImportacaoService
```

## Persistência

Responsável por efetivamente gravar os dados.

```text
ImportacaoPersistenciaService
```

Essa separação evita misturar validação com persistência.

---

# 43. Fluxo de emissão manual

A emissão manual de autorização segue conceitualmente:

```text
Usuário
   |
   v
Informa CPF
   |
   +-- visitante encontrado
   |       |
   |       +-- dados preenchidos
   |
   +-- visitante inexistente
           |
           +-- novo cadastro

       +
       |
       v
    Empresa
       |
       v
    Veículo opcional
       |
       v
    Primeiro dia
       |
       v
    Último dia
       |
       v
    Status
       |
       v
    Validação de colisão
       |
       v
    Persistência
```

Na alteração de uma autorização, a validação de colisão ignora a própria autorização que está sendo editada.

---

# 44. Regra de colisão na edição

Ao editar uma autorização, a regra de colisão é aplicada quando o novo status participa de colisão.

O sistema procura outra autorização:

```text
mesmo CPF
+
status participante de colisão
+
período sobreposto
```

A autorização que está sendo editada é explicitamente excluída da consulta.

Se houver outra autorização conflitante, a alteração é rejeitada.

---

# 45. Regra de colisão na alteração de status

A alteração de status também considera colisão.

Quando o novo status possui:

```text
participa_colisao = true
```

o sistema verifica se já existe outra autorização do mesmo visitante para o mesmo período.

Isso significa que a mudança de um status que não participa de colisão para um status que participa pode ser bloqueada caso exista uma autorização conflitante.

---

# 46. Exemplo completo de colisão

Considere:

```text
Visitante:
CPF = 11111111111
```

Autorização existente:

```text
Status = Autorizada
participa_colisao = true

01/08/2026 -> 10/08/2026
```

Nova autorização importada:

```text
CPF = 11111111111

01/08/2026 -> 05/08/2026
```

A consulta encontra:

```text
mesmo CPF
01/08 <= 05/08
10/08 >= 01/08
participa_colisao = true
```

Resultado:

```text
COLISÃO
```

A linha é marcada como inválida.

---

# 47. Exemplo sem colisão

Autorização existente:

```text
01/08/2026 -> 10/08/2026
```

Nova:

```text
11/08/2026 -> 20/08/2026
```

Teste:

```text
01/08 <= 20/08  -> verdadeiro
10/08 >= 11/08  -> falso
```

Como as duas condições não são simultaneamente verdadeiras:

```text
não existe colisão
```

---

# 48. Exemplo de status que não participa de colisão

Considere uma autorização:

```text
CPF = 11111111111
Status = X
participa_colisao = false

01/08/2026 -> 10/08/2026
```

Outra autorização do mesmo visitante:

```text
Status = Autorizada
participa_colisao = true

05/08/2026 -> 15/08/2026
```

A primeira autorização não é considerada pela busca de colisão porque:

```text
participa_colisao = false
```

Consequentemente, ela não bloqueia a segunda autorização.

# 49. Cadastros de visitantes, empresas e veículos

Podem ser consultados na região de dashboard, no canto direito. Permitem corrigir as informações cadastrais se os usuários possuem as credenciais adequadas ("VISITANTE_EDITAR", "EMPRESA_EDITAR" e "VEICULO_EDITAR", respectivamente). Os dados também podem ser excluídos (se houver, respectivamente, as credenciais de "VISITANTE_EXCLUIR", "EMPRESA_EXCLUIR" e "VEICULO_EXCLUIR"). Porém, a exclusão apenas poderá ocorrer se não houver dependência dos registros com outros campos do banco de dados:

| Cadastro      | Pode excluir quando                                                           | Antes de excluir                                                                     |
| ------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Visitante** | Não existir nenhuma `autorizacao.id_visitante` apontando para ele             | Se existirem registros em `visitante_veiculo`, remover essas associações manualmente |
| **Empresa**   | Não existir `visitante.id_empresa` **e** não existir `autorizacao.id_empresa` | Nada                                                                                 |
| **Veículo**   | Não existir nenhuma associação em `visitante_veiculo`                         | Nada                                                                                 |
Para uma compreensão mais abrangente de tais regras, recomenda-se consulta ao esquema de dados da seção a seguir (seção 50 - "Modelo de dados resumido") 

---

# 50. Modelo de dados resumido

```text
┌───────────────┐
│    USUARIO    │
└───────┬───────┘
        │
        ├──────── TIPO_USUARIO
        ├──────── SETOR ─────── LOCAL
        └──────── CREDENCIAL ─── CREDENCIAL_PERMISSAO ─── PERMISSAO


┌───────────────┐
│   EMPRESA     │
└───────┬───────┘
        │
        ├──────── VISITANTE ─────── VISITANTE_VEICULO ───── VEICULO
        │              │
        │              └──────── AUTORIZACAO
        │
        └──────── AUTORIZACAO
                         │
                         ├──── STATUS_AUTORIZACAO
                         ├──── SETOR
                         ├──── VEICULO
                         └──── HISTORICO_AUTORIZACAO
```

---

# 51. Docker

O projeto possui um `Dockerfile` baseado em:

```text
python:3.12-slim
```

A aplicação é instalada no diretório:

```text
/app
```

As dependências são instaladas a partir de:

```text
requirements.txt
```

A aplicação expõe:

```text
8000
```

e é iniciada com:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

O Dockerfile também aceita os argumentos:

```text
HTTP_PROXY
HTTPS_PROXY
NO_PROXY
```

---

# 52. Banco de dados

O schema inicial encontra-se em:

```text
database/schema.sql
```

O arquivo deve ser executado em um banco vazio.

O schema cria:

- tabelas;
- sequências;
- chaves primárias;
- chaves estrangeiras;
- restrições de unicidade;
- views;
- funções;
- triggers.

---

# 53. Views principais

## autorizacao_consulta

View utilizada para consolidar as informações necessárias para consulta de autorizações.

Além dos dados da autorização, calcula:

```text
status_exibicao
```

a partir de:

```text
status armazenado
+
primeiro_dia
+
ultimo_dia
+
CURRENT_DATE
```

## painel_autorizacao

Agrupa:

```text
status_exibicao
```

e calcula:

```text
quantidade
```

para cada estado.

---

# 54. Regras de negócio essenciais

As regras mais importantes do sistema podem ser resumidas assim.

### Visitante

```text
CPF identifica o visitante.
CPF é único.
```

### Empresa

```text
Empresa é entidade independente.
Nome da empresa é único.
```

### Autorização

```text
Uma autorização pertence a um visitante.
Uma autorização possui empresa própria.
Uma autorização possui período.
Uma autorização possui status.
```

### Colisão

```text
Mesmo CPF
+
períodos sobrepostos
+
status existente participa_colisao
=
colisão
```

### Importação

```text
Mesmo CPF na mesma planilha
+
nomes diferentes
=
erro

Mesmo CPF na mesma planilha
+
empresas diferentes
=
erro
```

### Cadastro existente

```text
CPF existente
+
nome diferente
=
aviso

CPF existente
+
empresa diferente
=
empresa do visitante atualizada
```

### Status

```text
Autorizada + futuro
    = Pendente

Autorizada + período vigente
    = Autorizada

Autorizada + período terminado
    = Expirada
```

---

# 54. Estrutura conceitual do projeto

A estrutura do backend segue a separação:

```text
app.py

controllers/
models/
repositories/
services/
security/
utils/
config/
database/

templates/
static/
```

A organização separa:

- interface HTTP;
- modelos;
- regras de negócio;
- acesso ao banco;
- segurança;
- utilitários;
- apresentação.

---

# 55. Princípios de manutenção

Ao alterar o sistema, as regras abaixo devem ser preservadas:

1. Não usar empresa como identificador do visitante.
2. CPF continua sendo o identificador do visitante.
3. Não confundir empresa do visitante com empresa da autorização.
4. Não transformar `Pendente` e `Expirada` em estados persistidos sem alterar explicitamente a regra de negócio.
5. Não remover a regra `participa_colisao` da verificação de conflitos.
6. Não considerar empresas ou veículos como parte da chave de colisão.
7. Não considerar uma autorização com `participa_colisao = false` como bloqueadora.
8. Ao editar uma autorização, ignorar a própria autorização na busca de colisão.
9. Não substituir automaticamente o nome cadastrado do visitante por causa de uma divergência na importação.
10. Manter a validação de coerência da planilha separada da verificação de colisão contra o banco.
11. A importação deve permanecer transacional.
12. Revogação deve ser tratada por mudança de status.

---

# 56. Resumo do fluxo de uma autorização

```text
                 ┌─────────────────────┐
                 │   Dados da pessoa   │
                 └──────────┬──────────┘
                            │
                            v
                    Identificação CPF
                            │
                 ┌──────────┴──────────┐
                 │                     │
             existente             inexistente
                 │                     │
                 v                     v
          reutiliza visitante      cria visitante
                 │                     │
                 └──────────┬──────────┘
                            │
                            v
                         Empresa
                            │
                            v
                    Veículo opcional
                            │
                            v
                         Período
                            │
                            v
                          Status
                            │
                            v
                   Verificação de
                       colisão
                            │
                    ┌───────┴───────┐
                    │               │
                 conflito        sem conflito
                    │               │
                    v               v
                  rejeita        persiste
                                    │
                                    v
                              registra histórico
```

---

# 57. Resumo do fluxo da importação

```text
                PLANILHA
                   |
                   v
              Normalização
                   |
                   v
             Linhas válidas
                   |
                   v
          Validação individual
                   |
          +--------+--------+
          |                 |
          v                 v
        Erros             OK
          |                 |
          |                 v
          |          Colisão com banco
          |                 |
          |          +------+------+
          |          |             |
          |          v             v
          |       colisão      sem colisão
          |          |             |
          |          v             v
          |       inválida       OK
          |                        |
          +-----------+------------+
                      |
                      v
             Coerência interna
               da planilha
                      |
          +-----------+-----------+
          |                       |
          v                       v
     inconsistência             OK
          |                       |
          v                       v
       inválida             pré-visualização
                                  |
                                  v
                            correções manuais
                                  |
                                  v
                              revalidação
                                  |
                                  v
                              confirmação
                                  |
                                  v
                              transação
                                  |
                         +--------+--------+
                         |                 |
                         v                 v
                       COMMIT           ROLLBACK
```

---

# 58. Regra fundamental da importação

A importação não deve ser entendida simplesmente como:

```text
"ler planilha e inserir registros"
```

Ela possui três níveis independentes de consistência:

```text
1. Consistência da própria linha
       |
       +-- CPF
       +-- Nome
       +-- Datas
       +-- demais campos

2. Consistência entre linhas da mesma planilha
       |
       +-- mesmo CPF não pode ter nomes diferentes
       +-- mesmo CPF não pode ter empresas diferentes

3. Consistência com o banco
       |
       +-- nome divergente = aviso
       +-- colisão de período = erro
```

Essa separação é fundamental para compreender o comportamento do sistema.

---

# 59. Observação sobre os estados derivados

`Pendente` e `Expirada` devem ser tratados como **estados de apresentação derivados do status persistido `Autorizada` e das datas atuais**.

Consequentemente, a mesma autorização pode mudar de estado de exibição sem que nenhum registro seja alterado no banco.

Por exemplo:

```text
01/08/2026
```

Uma autorização:

```text
primeiro_dia = 10/08/2026
ultimo_dia   = 20/08/2026
status       = Autorizada
```

será exibida como:

```text
Pendente
```

Em:

```text
15/08/2026
```

a mesma autorização será exibida como:

```text
Autorizada
```

Depois de:

```text
20/08/2026
```

passará a ser exibida como:

```text
Expirada
```

sem que o `id_status_autorizacao` necessariamente tenha sido alterado.

---

# 60. API

O projeto conta com API próprio para facilitar a integração a outros sistemas. Acessar url /docs para verificar Swagger da API desenvolvida (conforme disponibilizado pela biblioteca FastAPI).

# 61. Conclusão

## Sobre a organização do código

O projeto procura seguir os seguintes princípios:

- responsabilidade única por classe;
- separação entre regras de negócio e persistência;
- reutilização de serviços;
- transações explícitas;
- código organizado em camadas;
- baixa duplicação de lógica.

A arquitetura separa controllers, services e repositories, mantendo as regras de negócio concentradas nos serviços e o acesso ao PostgreSQL nos repositories.

## Sobre a principal funcionalidade do sistema: a importação em lote

O sistema é estruturado em torno do controle de autorizações de acesso, tendo o CPF como principal identificador do visitante e o período da autorização como elemento central das regras de conflito.

A importação em lote possui mecanismos próprios de:

- normalização;
- validação;
- coerência interna;
- verificação de colisões;
- pré-visualização;
- revalidação;
- persistência transacional.

As regras de colisão são baseadas exclusivamente na identidade do visitante, no período e na propriedade `participa_colisao` do status.

Os estados `Pendente` e `Expirada` são derivados de `Autorizada` conforme as datas da autorização e a data atual, enquanto outros estados correspondem diretamente ao status armazenado.

#### Sistema desenvolvido por: CT(EN) Guilherme VIEIRA DANTAS, BNIC

