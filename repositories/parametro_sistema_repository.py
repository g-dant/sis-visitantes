from config.database import (
  get_connection
)


class ParametroSistemaRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            chave,
            valor
          FROM parametro_sistema
          ORDER BY id
          """
        )

        return cursor.fetchall()

    finally:

      conn.close()


  @staticmethod
  def buscar_por_id(
    id_parametro_sistema: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            chave,
            valor
          FROM parametro_sistema
          WHERE id = %s
          """,
          (id_parametro_sistema,)
        )

        return cursor.fetchone()

    finally:

      conn.close()


  @staticmethod
  def buscar_por_chave(
    chave: str
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            chave,
            valor
          FROM parametro_sistema
          WHERE chave = %s
          """,
          (chave,)
        )

        return cursor.fetchone()

    finally:

      conn.close()


  @staticmethod
  def inserir(
    chave: str,
    valor: str
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO parametro_sistema (
            chave,
            valor
          )
          VALUES (%s, %s)
          RETURNING id
          """,
          (
            chave,
            valor
          )
        )

        resultado = cursor.fetchone()

        conn.commit()

        return resultado["id"]

    finally:

      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_parametro_sistema: int,
    chave: str,
    valor: str
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE parametro_sistema
          SET
            chave = %s,
            valor = %s
          WHERE id = %s
          """,
          (
            chave,
            valor,
            id_parametro_sistema
          )
        )

        conn.commit()

    finally:

      conn.close()


  @staticmethod
  def excluir(
    id_parametro_sistema: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM parametro_sistema
          WHERE id = %s
          """,
          (id_parametro_sistema,)
        )

        conn.commit()

    finally:

      conn.close()
