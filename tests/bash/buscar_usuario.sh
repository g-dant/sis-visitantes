#!/bin/bash

TOKEN=$(python3 -c "import json; print(json.load(open('token.json'))['token'])")

read -p "ID do usuário: " ID

curl --noproxy '*' -s \
  -X GET \
  "http://127.0.0.1:8000/usuarios/$ID" \
  -H "Authorization: Bearer $TOKEN"

echo
