curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Primera tarea actualizada",
  "description": "Descripción actualizada",
  "status": "En Proceso"
}'