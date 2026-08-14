#!/bin/bash

TOKEN=$(python3 -c "import json; print(json.load(open('token.json'))['token'])")

curl --noproxy '*' -s \
  -X GET \
  "http://127.0.0.1:8000/usuarios" \
  -H "Authorization: Bearer $TOKEN"

echo
