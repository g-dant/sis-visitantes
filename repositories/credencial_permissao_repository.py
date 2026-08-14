from config.database import get_connection


class CredencialPermissaoRepository:

  @staticmethod
  def possui_permissao(id_credencial: int, codigo_permissao: str):

    conn = get_connection()

    try:
      with conn.cursor() as cursor:
        cursor.execute(
          """
          SELECT 1 FROM 
          credencial_permissao cp
          JOIN 
          permissao p
          ON p.id = cp.id_permissao
          WHERE
          cp.id_credencial = %s
          AND p.codigo = %s
          LIMIT 1
          """,
          (id_credencial, codigo_permissao))

        return (cursor.fetchone() is not None)

    finally:
      conn.close()


  @staticmethod
  def listar_permissoes(id_credencial: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT p.codigo
          FROM credencial_permissao cp
          JOIN permissao p
            ON p.id = cp.id_permissao
          WHERE cp.id_credencial = %s
          ORDER BY p.codigo
          """,
          (id_credencial,))

        return [registro["codigo"]
          for registro in cursor.fetchall()]

    finally:
      conn.close()

