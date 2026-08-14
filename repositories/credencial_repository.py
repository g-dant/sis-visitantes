from config.database import get_connection


class CredencialRepository:

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
            ativo
          FROM credencial
          ORDER BY nome
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_credencial: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            nome,
            ativo
          FROM credencial
          WHERE id = %s
          """,
          (id_credencial,)
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    nome: str,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO credencial (
            nome,
            ativo
          )
          VALUES (
            %s,
            %s
          )
          RETURNING id
          """,
          (
            nome,
            ativo
          )
        )

        id_credencial = cursor.fetchone()["id"]

        conn.commit()

        return id_credencial

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_credencial: int,
    nome: str,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE credencial
          SET
            nome = %s,
            ativo = %s
          WHERE id = %s
          """,
          (
            nome,
            ativo,
            id_credencial
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_credencial: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM credencial
          WHERE id = %s
          """,
          (id_credencial,)
        )

        conn.commit()

    finally:
      conn.close()
