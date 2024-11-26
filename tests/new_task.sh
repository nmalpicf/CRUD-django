#!/bin/bash

curl -X POST http://127.0.0.1:8000/api/tasks/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Quinta tarea",
  "description": "Esta es la quinta tarea"
}'