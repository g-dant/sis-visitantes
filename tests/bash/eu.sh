#!/bin/bash
TOKEN=$(jq -r '.token' token.json)
curl --noproxy '*' -s -X GET "http://127.0.0.1:8000/eu" -H "Authorization: Bearer $TOKEN"
echo
