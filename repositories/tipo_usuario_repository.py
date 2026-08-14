from config.database import get_connection


class TipoUsuarioRepository:

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
          FROM tipo_usuario
          ORDER BY nome
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_tipo: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id,
            nome,
            ativo
          FROM tipo_usuario
          WHERE id = %s
          """,
          (id_tipo,)
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
          INSERT INTO tipo_usuario (
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

        id_tipo = cursor.fetchone()["id"]

        conn.commit()

        return id_tipo

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_tipo: int,
    nome: str,
    ativo: bool
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE tipo_usuario
          SET
            nome = %s,
            ativo = %s
          WHERE id = %s
          """,
          (
            nome,
            ativo,
            id_tipo
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_tipo: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM tipo_usuario
          WHERE id = %s
          """,
          (id_tipo,)
        )

        conn.commit()

    finally:
      conn.close()
