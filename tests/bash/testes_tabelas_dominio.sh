#!/bin/bash

TOKEN=$(python3 -c "import json; print(json.load(open('tests/bash/token.json'))['token'])")

BASE_URL="http://127.0.0.1:8000"

linha() {
  printf "\n============================================================\n"
}

titulo() {
  linha
  echo "$1"
  linha
}

etapa() {
  echo
  echo ">>> $1"
}

#
# TIPO_USUARIO
#

titulo "TIPO_USUARIO"

etapa "Criando"

RESPOSTA=$(curl --noproxy '*' -s \
  -X POST "$BASE_URL/tipos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Tipo Teste","ativo":true}')

echo "$RESPOSTA"

ID_TIPO=$(echo "$RESPOSTA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

etapa "Atualizando"

curl --noproxy '*' -s \
  -X PUT "$BASE_URL/tipos/$ID_TIPO" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Tipo Teste Alterado","ativo":true}'

echo

etapa "Buscando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/tipos/$ID_TIPO" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Excluindo"

curl --noproxy '*' -s \
  -X DELETE "$BASE_URL/tipos/$ID_TIPO" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Listando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/tipos" \
  -H "Authorization: Bearer $TOKEN"

echo

#
# CREDENCIAL
#

titulo "CREDENCIAL"

etapa "Criando"

RESPOSTA=$(curl --noproxy '*' -s \
  -X POST "$BASE_URL/credenciais" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Credencial Teste","ativo":true}')

echo "$RESPOSTA"

ID_CREDENCIAL=$(echo "$RESPOSTA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

etapa "Atualizando"

curl --noproxy '*' -s \
  -X PUT "$BASE_URL/credenciais/$ID_CREDENCIAL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Credencial Alterada","ativo":true}'

echo

etapa "Buscando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/credenciais/$ID_CREDENCIAL" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Excluindo"

curl --noproxy '*' -s \
  -X DELETE "$BASE_URL/credenciais/$ID_CREDENCIAL" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Listando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/credenciais" \
  -H "Authorization: Bearer $TOKEN"

echo

#
# LOCAL
#

titulo "LOCAL"

etapa "Criando"

RESPOSTA=$(curl --noproxy '*' -s \
  -X POST "$BASE_URL/locais" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"codigo":"LOC-TST","descricao":"Local Teste","ativo":true}')

echo "$RESPOSTA"

ID_LOCAL=$(echo "$RESPOSTA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

etapa "Atualizando"

curl --noproxy '*' -s \
  -X PUT "$BASE_URL/locais/$ID_LOCAL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"codigo":"LOC-ALT","descricao":"Local Alterado","ativo":true}'

echo

etapa "Buscando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/locais/$ID_LOCAL" \
  -H "Authorization: Bearer $TOKEN"

echo

#
# STATUS_AUTORIZACAO
#

titulo "STATUS_AUTORIZACAO"

etapa "Criando"

RESPOSTA=$(curl --noproxy '*' -s \
  -X POST "$BASE_URL/status-autorizacoes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Status Teste","descricao":"Status criado pelo teste","ativo":true}')

echo "$RESPOSTA"

ID_STATUS=$(echo "$RESPOSTA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

etapa "Atualizando"

curl --noproxy '*' -s \
  -X PUT "$BASE_URL/status-autorizacoes/$ID_STATUS" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Status Alterado","descricao":"Status alterado","ativo":true}'

echo

etapa "Buscando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/status-autorizacoes/$ID_STATUS" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Excluindo"

curl --noproxy '*' -s \
  -X DELETE "$BASE_URL/status-autorizacoes/$ID_STATUS" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Listando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/status-autorizacoes" \
  -H "Authorization: Bearer $TOKEN"

echo

#
# SETOR
#

titulo "SETOR"

etapa "Criando"

RESPOSTA=$(curl --noproxy '*' -s \
  -X POST "$BASE_URL/setores" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"codigo\":\"SET-TST\",\"descricao\":\"Setor Teste\",\"ativo\":true,\"id_local\":$ID_LOCAL}")

echo "$RESPOSTA"

ID_SETOR=$(echo "$RESPOSTA" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

etapa "Atualizando"

curl --noproxy '*' -s \
  -X PUT "$BASE_URL/setores/$ID_SETOR" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"codigo\":\"SET-ALT\",\"descricao\":\"Setor Alterado\",\"ativo\":true,\"id_local\":$ID_LOCAL}"

echo

etapa "Buscando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/setores/$ID_SETOR" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Excluindo"

curl --noproxy '*' -s \
  -X DELETE "$BASE_URL/setores/$ID_SETOR" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Listando"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/setores" \
  -H "Authorization: Bearer $TOKEN"

echo

#
# LIMPEZA
#

titulo "LIMPEZA"

etapa "Excluindo Local"

curl --noproxy '*' -s \
  -X DELETE "$BASE_URL/locais/$ID_LOCAL" \
  -H "Authorization: Bearer $TOKEN"

echo

etapa "Listando Locais"

curl --noproxy '*' -s \
  -X GET "$BASE_URL/locais" \
  -H "Authorization: Bearer $TOKEN"

echo

titulo "TESTE FINALIZADO"
