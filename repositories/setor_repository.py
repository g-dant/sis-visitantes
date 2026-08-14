from config.database import get_connection


class SetorRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            s.id,
            s.codigo,
            s.descricao,
            s.ativo,

            s.id_local,
            l.codigo AS local_codigo,
            l.descricao AS local_descricao

          FROM setor s

          JOIN local l
            ON l.id = s.id_local

          ORDER BY s.descricao
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_setor: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            s.id,
            s.codigo,
            s.descricao,
            s.ativo,

            s.id_local,
            l.codigo AS local_codigo,
            l.descricao AS local_descricao

          FROM setor s

          JOIN local l
            ON l.id = s.id_local

          WHERE s.id = %s
          """,
          (id_setor,)
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    codigo: str,
    descricao: str,
    ativo: bool,
    id_local: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO setor (
            codigo,
            descricao,
            ativo,
            id_local
          )
          VALUES (
            %s,
            %s,
            %s,
            %s
          )
          RETURNING id
          """,
          (
            codigo,
            descricao,
            ativo,
            id_local
          )
        )

        id_setor = cursor.fetchone()["id"]

        conn.commit()

        return id_setor

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_setor: int,
    codigo: str,
    descricao: str,
    ativo: bool,
    id_local: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE setor
          SET
            codigo = %s,
            descricao = %s,
            ativo = %s,
            id_local = %s
          WHERE id = %s
          """,
          (
            codigo,
            descricao,
            ativo,
            id_local,
            id_setor
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_setor: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM setor
          WHERE id = %s
          """,
          (id_setor,)
        )

        conn.commit()

    finally:
      conn.close()
