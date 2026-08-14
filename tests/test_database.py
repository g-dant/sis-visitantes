from config.database import get_connection

try:

  conn = get_connection()

  print("Conectado ao PostgreSQL!")

  conn.close()

except Exception as e:

  print("Erro:")
  print(e)
