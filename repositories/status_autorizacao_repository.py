from config.database import get_connection


class StatusAutorizacaoRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            nome,
            descricao,
            ativo
          FROM status_autorizacao
          ORDER BY nome
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_status: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            nome,
            descricao,
            ativo,
            participa_colisao
          FROM status_autorizacao
          WHERE id = %s
          """,
          (id_status,)
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    nome: str,
    descricao: str | None,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO status_autorizacao (
            nome,
            descricao,
            ativo
          )
          VALUES (
            %s,
            %s,
            %s
          )
          RETURNING id
          """,
          (
            nome,
            descricao,
            ativo
          )
        )

        id_status = cursor.fetchone()["id"]

        conn.commit()

        return id_status

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_status: int,
    nome: str,
    descricao: str | None,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE status_autorizacao
          SET
            nome = %s,
            descricao = %s,
            ativo = %s
          WHERE id = %s
          """,
          (
            nome,
            descricao,
            ativo,
            id_status
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_status: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM status_autorizacao
          WHERE id = %s
          """,
          (id_status,)
        )

        conn.commit()

    finally:
      conn.close()
