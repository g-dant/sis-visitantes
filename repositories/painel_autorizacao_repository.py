from psycopg2.extras import RealDictCursor
from config.database import get_connection


class PainelAutorizacaoRepository:

  @staticmethod
  def buscar():

    conn = get_connection()

    try:
      with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
          SELECT
            status_exibicao,
            quantidade
          FROM painel_autorizacao
          """)

        return cursor.fetchall()

    finally:
      conn.close()
