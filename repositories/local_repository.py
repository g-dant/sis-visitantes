from config.database import get_connection


class LocalRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            codigo,
            descricao,
            ativo
          FROM local
          ORDER BY descricao
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_local: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            codigo,
            descricao,
            ativo
          FROM local
          WHERE id = %s
          """,
          (id_local,)
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    codigo: str,
    descricao: str,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO local (
            codigo,
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
            codigo,
            descricao,
            ativo
          )
        )

        id_local = cursor.fetchone()["id"]

        conn.commit()

        return id_local

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_local: int,
    codigo: str,
    descricao: str,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE local
          SET
            codigo = %s,
            descricao = %s,
            ativo = %s
          WHERE id = %s
          """,
          (
            codigo,
            descricao,
            ativo,
            id_local
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_local: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM local
          WHERE id = %s
          """,
          (id_local,)
        )

        conn.commit()

    finally:
      conn.close()
