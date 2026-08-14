#!/bin/bash

TOKEN=$(python3 -c "import json; print(json.load(open('tests/bash/token.json'))['token'])")

read -p "ID do usuário: " ID

curl --noproxy '*' -s \
  -X PUT \
  "http://127.0.0.1:8000/usuarios/$ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome":"Usuario Atualizado",
    "email":"usuario.atualizado@empresa.com",
    "telefone":"21888888888",
    "id_tipo":1,
    "id_setor":1,
    "id_credencial":1
  }'

echo
