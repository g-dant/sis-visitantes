import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST_SISVISITANTES")
DB_PORT = os.getenv("DB_PORT_SISVISITANTES")
DB_NAME = os.getenv("DB_NAME_SISVISITANTES")
DB_USER = os.getenv("DB_USER_SISVISITANTES")
DB_PASSWORD = os.getenv("DB_PASSWORD_SISVISITANTES")

def get_connection():
  return psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    cursor_factory=RealDictCursor)
