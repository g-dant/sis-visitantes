#!/bin/bash

echo -n "Email: "
read EMAIL
read -s -p "Senha: " SENHA

echo
curl --noproxy 127.0.0.1 -s -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d "{\"email\":\"$EMAIL\",\"senha\":\"$SENHA\"}" | tee token.json
echo
