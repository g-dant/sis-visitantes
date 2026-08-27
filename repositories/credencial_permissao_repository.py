from config.database import get_connection


class CredencialPermissaoRepository:

  @staticmethod
  def possui_permissao(id_credencial: int, codigo_permissao: str):

    conn = get_connection()

    try:
      with conn.cursor() as cursor:
        cursor.execute("""
          SELECT 1 FROM 
          credencial_permissao cp
          JOIN 
          permissao p
          ON p.id = cp.id_permissao
          WHERE
          cp.id_credencial = %s
          AND p.codigo = %s
          LIMIT 1
          """, (id_credencial, codigo_permissao))

        return (cursor.fetchone() is not None)

    finally:
      conn.close()


  @staticmethod
  def listar_permissoes(id_credencial: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT p.codigo
          FROM credencial_permissao cp
          JOIN permissao p
            ON p.id = cp.id_permissao
          WHERE cp.id_credencial = %s
          ORDER BY p.codigo
          """, (id_credencial,))

        return [registro["codigo"]
          for registro in cursor.fetchall()]

    finally:
      conn.close()
      
  @staticmethod
  def inserir(
    id_credencial: int,
    id_permissao: int,
    conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO credencial_permissao (
            id_credencial,
            id_permissao
          ) VALUES (
            %s,
            %s)""", (
            id_credencial,
            id_permissao))

      if not conn_externa:
        conn.commit()

    finally:
      if not conn_externa:
        conn.close()

  @staticmethod
  def excluir_por_credencial(id_credencial: int, conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM credencial_permissao
          WHERE id_credencial = %s
          """, (id_credencial,))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()
        
  @staticmethod
  def listar_todas_permissoes():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
            id,
            codigo,
            descricao
          FROM permissao
          ORDER BY codigo""")

        return cursor.fetchall()

    finally:
      conn.close()
      
  @staticmethod
  def listar_permissoes_com_status(id_credencial: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
            p.id,
            p.codigo,
            p.descricao,
            CASE
              WHEN cp.id IS NOT NULL
              THEN true
              ELSE false
            END AS habilitado
          FROM permissao p
          LEFT JOIN credencial_permissao cp
            ON cp.id_permissao = p.id
            AND cp.id_credencial = %s
          ORDER BY p.codigo""",
          (id_credencial,)
        )

        return cursor.fetchall()

    finally:
      conn.close()
      
  @staticmethod
  def excluir_por_credencial_e_permissao(
    id_credencial: int,
    id_permissao: int,
    conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM credencial_permissao
          WHERE
            id_credencial = %s
            AND id_permissao = %s
          """, (
            id_credencial,
            id_permissao))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()
