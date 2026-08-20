from config.database import get_connection


class HistoricoAutorizacaoRepository:

  @staticmethod
  def listar_por_autorizacao(id_autorizacao: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            h.id,
            h.id_autorizacao,

            h.id_usuario,
            u.nome AS usuario_nome,

            h.data_hora,
            h.descricao

          FROM historico_autorizacao h

          JOIN usuario u
            ON u.id = h.id_usuario

          WHERE h.id_autorizacao = %s

          ORDER BY h.data_hora
          """,
          (id_autorizacao,))

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def inserir(id_autorizacao: int, id_usuario: int, descricao: str, conn=None):

    conn_externa = conn is not None
    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO historico_autorizacao (
            id_autorizacao,
            id_usuario,
            descricao)
          VALUES (%s, %s, %s)
          RETURNING id
          """, (id_autorizacao, id_usuario, descricao))

        id_historico = cursor.fetchone()["id"]

        if not conn_externa:
          conn.commit()

        return id_historico

    finally:
      if not conn_externa:  
        conn.close()
