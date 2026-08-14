# Manual do Usuário — Sistema de Controle de Visitantes

## 1. Sobre o sistema

O Sistema de Controle de Visitantes permite gerenciar:

- visitantes;
- empresas;
- veículos;
- autorizações de acesso;
- usuários;
- setores;
- locais;
- credenciais e permissões.

As autorizações podem ser cadastradas individualmente ou por importação em lote através de planilhas.

Também é possível consultar autorizações, acompanhar seus estados, alterar autorizações e consultar o histórico das operações.

---

# 2. Acesso ao sistema

O acesso é realizado por usuário e senha.

As funcionalidades disponíveis dependem das permissões associadas ao usuário.

O usuário também está associado a um setor, que determina seu contexto dentro da organização.

---

# 3. Usuários

A tela de usuários permite administrar os usuários que podem acessar o sistema.

Um usuário possui informações como:

- nome;
- e-mail;
- telefone;
- tipo de usuário;
- setor;
- credencial;
- senha;
- situação ativa/inativa.

É possível:

- cadastrar usuário;
- alterar usuário;
- ativar ou desativar usuário;
- consultar usuários;
- alterar credenciais.

As permissões disponíveis dependem da credencial atribuída ao usuário.

---

# 4. Empresas

As empresas representam as organizações às quais os visitantes estão vinculados.

É possível:

- cadastrar empresa;
- consultar empresa;
- alterar empresa;
- ativar ou desativar empresa.

A empresa possui, entre outros dados:

- nome;
- CNPJ;
- situação.

O nome da empresa é utilizado para identificar uma empresa durante a importação em lote.

---

# 5. Visitantes

O cadastro do visitante contém:

- nome;
- CPF;
- RG;
- e-mail;
- celular;
- empresa;
- situação ativa/inativa.

O **CPF é o principal identificador do visitante** e é único no sistema.

Assim, o mesmo CPF representa a mesma pessoa no cadastro, independentemente da empresa informada em uma autorização.

---

# 6. Veículos

Um visitante pode utilizar um veículo em uma autorização.

O cadastro do veículo possui:

- placa;
- marca;
- tipo/modelo;
- cor;
- observações;
- situação.

A placa identifica o veículo.

Na autorização, o veículo é opcional.

---

# 7. Autorizações

Uma autorização determina quando e em que condições um visitante poderá acessar o local.

Cada autorização possui:

- visitante;
- empresa;
- setor solicitante;
- primeiro dia;
- último dia;
- status;
- veículo opcional.

A empresa da autorização é registrada separadamente da empresa atualmente associada ao cadastro do visitante.

---

# 8. Cadastro de uma autorização

Para cadastrar uma autorização, informe os dados solicitados, principalmente:

1. visitante;
2. empresa;
3. período de validade;
4. veículo, se houver;
5. demais informações solicitadas pela tela.

O sistema verifica se existe conflito com outra autorização do mesmo visitante.

---

# 9. Colisão de autorizações

Uma colisão ocorre quando o mesmo visitante possui duas autorizações com períodos sobrepostos e a autorização já existente possui um status que participa da verificação de colisão.

A comparação é feita pelo **CPF**.

A empresa e o veículo não definem se existe colisão.

## Exemplo

Autorização existente:

```text
01/08/2026 até 10/08/2026
```

Nova autorização:

```text
05/08/2026 até 15/08/2026
```

Há colisão porque os períodos se sobrepõem.

Também há colisão quando uma autorização começa exatamente no dia em que outra termina:

```text
01/08/2026 até 10/08/2026
10/08/2026 até 20/08/2026
```

O dia 10 pertence aos dois períodos.

## Sem colisão

```text
01/08/2026 até 10/08/2026
11/08/2026 até 20/08/2026
```

Nesse caso não há sobreposição.

---

# 10. Status das autorizações

O sistema possui uma diferença importante entre o status cadastrado e o estado apresentado na consulta.

O status `Autorizada` pode aparecer na tela como diferentes estados, dependendo das datas.

## Pendente

Uma autorização com status armazenado `Autorizada` aparece como:

```text
Pendente
```

quando seu primeiro dia ainda não chegou.

Exemplo:

```text
Hoje:          05/08
Primeiro dia:  10/08
```

A autorização está emitida, mas ainda não começou a valer.

## Autorizada

Quando:

```text
primeiro_dia <= hoje <= ultimo_dia
```

a autorização é apresentada como:

```text
Autorizada
```

Isso significa que o período está vigente.

## Expirada

Quando o último dia já passou:

```text
ultimo_dia < hoje
```

a autorização é apresentada como:

```text
Expirada
```

A autorização continua registrada no sistema, mas seu período de validade terminou.

## Outros estados

Outros status cadastrados, como `Revogada`, são apresentados diretamente pelo seu nome.

Uma autorização revogada, por exemplo, permanece registrada e pode ser consultada.

### Resumo

| Situação | Estado apresentado |
|---|---|
| `Autorizada` e ainda não começou | Pendente |
| `Autorizada` e vigente | Autorizada |
| `Autorizada` e período encerrado | Expirada |
| Outro status | Nome do status |

`Pendente` e `Expirada` são estados derivados das datas. Não é necessário alterar manualmente o status da autorização para que ela passe de Pendente para Autorizada ou de Autorizada para Expirada.

---

# 11. Revogação

Revogar uma autorização é diferente de excluí-la.

A revogação altera o status da autorização.

A autorização continua armazenada e seu histórico permanece disponível.

A exclusão é uma operação distinta.

---

# 12. Alteração de autorização

Uma autorização existente pode ser alterada conforme as permissões do usuário.

Entre os dados que podem ser alterados estão:

- período;
- status;
- visitante;
- veículo.

Ao alterar uma autorização, o sistema verifica novamente possíveis colisões.

A própria autorização que está sendo alterada não é considerada como uma colisão consigo mesma.

As alterações são registradas no histórico.

---

# 13. Histórico

O histórico permite acompanhar o que aconteceu com uma autorização.

Entre os eventos registrados estão:

- criação;
- criação por importação em lote;
- alteração de status;
- alteração de período;
- exclusão.

Os registros informam o usuário responsável e a data/hora da operação.

---

# 14. Importação em lote

A importação permite cadastrar várias autorizações a partir de uma única planilha.

Formatos aceitos:

- CSV;
- XLSX;
- ODS.

A importação possui quatro grandes etapas:

```text
Planilha
   ↓
Validação
   ↓
Revisão
   ↓
Confirmação
```

Nenhum dado é gravado durante a etapa inicial de validação.

---

# 15. Campos da planilha

A planilha utiliza os seguintes dados:

| Campo | Obrigatório |
|---|---|
| CPF | Sim |
| Nome | Sim |
| Empresa | Sim |
| Placa | Não |
| De / Primeiro Dia | Sim |
| Até / Último Dia | Sim |

Linhas completamente vazias são ignoradas.

---

# 16. Validação da planilha

Antes da importação, cada linha é validada.

São verificadas, entre outras coisas:

- CPF informado;
- CPF válido;
- nome informado;
- datas informadas;
- placa;
- coerência entre linhas;
- divergências em relação ao cadastro existente;
- colisões de autorização.

Erros impedem a importação da linha.

Avisos são apresentados ao usuário, mas não necessariamente impedem a importação.

---

# 17. Regras para o mesmo CPF na planilha

O CPF identifica a pessoa.

Por isso, todas as ocorrências do mesmo CPF dentro de uma mesma planilha devem ser coerentes.

## Mesmo CPF com nomes diferentes

Exemplo:

```text
CPF 111 — João Silva
CPF 111 — João Souza
```

Resultado:

```text
ERRO
```

As linhas são consideradas inconsistentes.

## Mesmo CPF com empresas diferentes

Exemplo:

```text
CPF 111 — Empresa A
CPF 111 — Empresa B
```

Resultado:

```text
ERRO
```

As linhas são consideradas inconsistentes.

## Mesmo CPF com mesmo nome e mesma empresa

Exemplo:

```text
CPF 111 — João Silva — Empresa A
CPF 111 — João Silva — Empresa A
```

Não existe, por si só, uma inconsistência de identidade.

As demais regras, especialmente as de colisão de períodos, continuam sendo aplicadas.

---

# 18. Divergência entre a planilha e o cadastro existente

Existe uma diferença importante entre uma inconsistência dentro da planilha e uma divergência em relação ao banco.

## Nome diferente do cadastro

Exemplo:

```text
Cadastro:
CPF 111 → João Silva

Planilha:
CPF 111 → João Souza
```

O sistema apresenta um aviso de nome divergente.

Isso **não significa automaticamente que o visitante será alterado**.

O nome cadastrado não é substituído automaticamente pelo nome da planilha.

## Empresa diferente do cadastro

Se o CPF já existe, o visitante existente é reutilizado.

Durante a persistência da importação, a empresa associada ao visitante é atualizada para a empresa informada na importação.

A nova autorização também recebe a empresa informada na linha.

Isso é diferente da regra de nomes: divergência de nome gera aviso; a empresa do visitante existente é atualizada.

---

# 19. Empresas na importação

Ao confirmar a importação:

- se a empresa já existir, ela será reutilizada;
- se não existir, será criada automaticamente.

A busca da empresa é feita pelo nome.

---

# 20. Visitantes na importação

Ao confirmar a importação:

- o sistema procura o visitante pelo CPF;
- se encontrar, reutiliza o visitante;
- se não encontrar, cria um novo visitante.

Portanto, a importação não cria automaticamente uma nova pessoa apenas porque a empresa mudou.

O CPF continua sendo o identificador do visitante.

---

# 21. Veículos na importação

A placa é utilizada para localizar o veículo.

### Placa já cadastrada

O veículo existente é reutilizado.

### Placa inexistente

Um novo veículo é criado.

### Placa vazia

Nenhum veículo é associado à autorização.

---

# 22. Colisão durante a importação

A importação verifica colisões contra autorizações já existentes no banco.

Para uma linha, a verificação considera:

```text
mesmo CPF
+
período sobreposto
+
autorização existente com status participante de colisão
```

Se uma colisão for encontrada, a linha é marcada como inválida.

A empresa não elimina uma colisão.

Por exemplo:

```text
CPF 111 — Empresa A — 01/08 a 10/08

CPF 111 — Empresa B — 05/08 a 15/08
```

Continua existindo colisão porque o CPF é o mesmo.

---

# 23. Revisão da importação

Depois da validação, o sistema apresenta uma tabela de revisão.

Cada linha mostra:

- dados importados;
- resultado da validação;
- erros;
- avisos.

Uma linha válida pode ser identificada como:

```text
OK
```

Uma linha com problemas apresenta os erros encontrados.

---

# 24. Correção durante a revisão

Quando um campo apresenta erro, ele pode ser corrigido diretamente na tela de revisão.

Depois da alteração:

1. a linha é enviada novamente para validação;
2. as regras são executadas novamente;
3. o resultado é atualizado.

Assim, não é necessário começar toda a importação novamente para corrigir um campo.

---

# 25. Confirmação da importação

Depois que os dados estiverem válidos, a importação pode ser confirmada.

Para cada linha, o sistema:

1. localiza ou cria a empresa;
2. localiza ou cria o visitante pelo CPF;
3. localiza ou cria o veículo pela placa;
4. cria a autorização;
5. registra o histórico de criação por lote.

---

# 26. Segurança da importação

A confirmação da importação ocorre dentro de uma única transação.

Isso significa:

```text
todas as operações são confirmadas
```

ou:

```text
nenhuma operação é confirmada
```

Se ocorrer um erro durante a gravação, a transação é revertida.

Isso evita que um lote fique parcialmente gravado.

---

# 27. Status inicial da importação

As autorizações criadas pela importação utilizam o status definido pelo parâmetro:

```text
STATUS_AUTORIZACAO_LOTE_PADRAO
```

Assim, o status inicial do lote pode ser configurado sem alterar diretamente a lógica da importação.

---

# 28. Consulta de autorizações

A consulta permite visualizar informações como:

- visitante;
- CPF;
- empresa;
- veículo;
- período;
- status;
- setor;
- solicitante;
- histórico.

O estado apresentado na consulta considera também as datas atuais.

Por isso, uma autorização cadastrada como `Autorizada` pode aparecer como `Pendente` ou `Expirada`.

---

# 29. Leitura de QR Code

As autorizações podem ser exportadas em forma de QR Code.

O QR Code pode ser validado utilizando a webcam da estação, tablet ou smartphone em que o sistema estiver sendo utilizado.

Essa funcionalidade permite verificar uma autorização sem precisar localizar manualmente o registro na tela.

---

# 30. Dicas importantes

### O CPF identifica a pessoa

Não considere a empresa como parte da identidade do visitante.

```text
CPF = pessoa
```

A empresa pode mudar.

### Empresa diferente não significa pessoa diferente

Se o mesmo CPF aparecer associado a outra empresa, o sistema continua tratando-o como o mesmo visitante.

### Nome diferente exige atenção

Se o mesmo CPF aparecer com nomes diferentes na mesma planilha, a importação é bloqueada para essas linhas.

Se o nome da planilha for diferente do nome já cadastrado no banco, a situação é apresentada como aviso.

### Colisão depende do CPF e do período

A empresa e o veículo não tornam duas autorizações de um mesmo CPF independentes para fins de colisão.

### Pendente e Expirada são automáticos

Não é necessário alterar manualmente uma autorização de `Autorizada` para `Pendente` ou `Expirada`.

Esses estados são calculados de acordo com as datas.

### Revogar não é excluir

Uma autorização revogada continua registrada e pode ser consultada no histórico.

---

# 31. Fluxo recomendado para cadastrar uma autorização

```text
1. Localizar ou cadastrar o visitante
             ↓
2. Confirmar os dados do visitante
             ↓
3. Informar a empresa
             ↓
4. Informar o período
             ↓
5. Informar veículo, se houver
             ↓
6. Selecionar o status
             ↓
7. Confirmar
             ↓
8. Sistema verifica colisões
             ↓
9. Autorização é gravada
             ↓
10. Histórico é registrado
```

---

# 32. Fluxo recomendado para importação

```text
1. Preparar a planilha
        ↓
2. Importar arquivo
        ↓
3. Conferir erros e avisos
        ↓
4. Corrigir linhas inválidas
        ↓
5. Revalidar
        ↓
6. Conferir possíveis divergências
        ↓
7. Confirmar importação
        ↓
8. Sistema grava o lote em uma transação
```

---

# 33. Resumo das regras mais importantes

| Situação | Comportamento |
|---|---|
| CPF novo | Novo visitante pode ser criado |
| CPF existente | Visitante é reutilizado |
| Mesmo CPF + nomes diferentes na planilha | Erro |
| Mesmo CPF + empresas diferentes na planilha | Erro |
| CPF existente + nome diferente do banco | Aviso |
| CPF existente + empresa diferente | Empresa do visitante é atualizada |
| Empresa existente | Reutilizada |
| Empresa inexistente | Criada |
| Placa existente | Veículo reutilizado |
| Placa inexistente | Veículo criado |
| Placa vazia | Sem veículo |
| Mesmo CPF + período sobreposto + status participante | Colisão |
| CPFs diferentes | Não há colisão entre eles |
| Status não participante de colisão | Não bloqueia por colisão |
| `Autorizada` antes do início | Pendente |
| `Autorizada` durante o período | Autorizada |
| `Autorizada` após o período | Expirada |
| Revogada | Permanece registrada |
| Erro durante confirmação do lote | Toda a transação é revertida |

---

# 34. Glossário rápido

**Visitante**  
Pessoa identificada pelo CPF que poderá receber autorizações.

**Empresa**  
Organização associada ao visitante e/ou à autorização.

**Autorização**  
Registro que concede acesso a um visitante durante determinado período.

**Status armazenado**  
Status efetivamente cadastrado para a autorização.

**Status de exibição**  
Estado apresentado ao usuário, podendo ser derivado das datas.

**Pendente**  
Autorização `Autorizada` cujo período ainda não começou.

**Autorizada**  
Autorização `Autorizada` cujo período está vigente.

**Expirada**  
Autorização `Autorizada` cujo período já terminou.

**Revogada**  
Autorização cujo status foi alterado para um estado de revogação.

**Colisão**  
Sobreposição de períodos de autorizações do mesmo CPF quando a autorização existente participa da verificação de colisão.

**Importação em lote**  
Cadastro de várias autorizações a partir de uma planilha.

**Histórico**  
Registro das operações realizadas sobre uma autorização.

#### Sistema desenvolvido por CT(EN) Guilherme VIEIRA DANTAS, BNIC
