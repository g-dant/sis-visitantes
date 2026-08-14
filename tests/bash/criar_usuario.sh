#!/bin/bash

TOKEN=$(python3 -c "import json; print(json.load(open('tests/bash/token.json'))['token'])")

curl --noproxy '*' -s \
  -X POST \
  "http://127.0.0.1:8000/usuarios" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome":"Teste API",
    "email":"teste.api@empresa.com",
    "telefone":"21999999999",
    "id_tipo":1,
    "id_setor":1,
    "id_credencial":1,
    "senha":"123456"
  }'

echo
