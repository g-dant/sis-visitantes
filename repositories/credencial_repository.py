from config.database import get_connection


class CredencialRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
            c.id,
            c.nome,
            c.descricao,
            c.ativo,
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM usuario u
                WHERE u.id_credencial = c.id
              )
              THEN false
              ELSE true
            END AS pode_excluir
          FROM credencial c
          ORDER BY c.nome
          """)

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_credencial: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
            c.id,
            c.nome,
            c.descricao,
            c.ativo,
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM usuario u
                WHERE u.id_credencial = c.id
              )
              THEN false
              ELSE true
            END AS pode_excluir
          FROM credencial c
          WHERE c.id = %s
        """, (id_credencial,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    nome: str,
    descricao: str | None,
    ativo: bool,
    conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO credencial (
            nome,
            descricao,
            ativo)
          VALUES (
            %s,
            %s,
            %s)
          RETURNING id
          """,
          (nome,
           descricao,
           ativo
          ))

        id_credencial = cursor.fetchone()["id"]

      if not conn_externa:
        conn.commit()

      return id_credencial

    finally:
      if not conn_externa:
        conn.close()

  @staticmethod
  def atualizar_tudo(
    id_credencial: int, 
    nome: str, 
    descricao: str | None, 
    ativo: bool):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          UPDATE credencial
          SET
            nome = %s,
            descricao = %s,
            ativo = %s
          WHERE id = %s
          """, (
            nome,
            descricao,
            ativo,
            id_credencial))

        conn.commit()

    finally:
      conn.close()

  @staticmethod
  def excluir(id_credencial: int, conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM credencial
          WHERE id = %s
          """, (id_credencial,))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()
