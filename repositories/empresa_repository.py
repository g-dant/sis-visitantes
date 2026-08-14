from config.database import get_connection


class EmpresaRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
          id, nome, cnpj, ativo
          FROM empresa
          ORDER BY nome
          """)

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_empresa: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
          id, nome, cnpj, ativo
          FROM empresa
          WHERE id = %s
          """,
          (id_empresa,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    nome: str,
    cnpj: str,
    ativo: bool,
    conn=None):

    conn_externa = (conn is not None)
    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:
        cursor.execute(
          """
          INSERT INTO empresa 
          (nome, cnpj, ativo)
          VALUES 
          (%s, %s, %s)
          RETURNING id
          """,
          (nome, cnpj, ativo))

        id_empresa = cursor.fetchone()["id"]
        
        if not conn_externa:
          conn.commit()

        return id_empresa

    finally:
      if not conn_externa:
        conn.close()


  @staticmethod
  def atualizar_tudo(
    id_empresa: int,
    nome: str,
    cnpj: str,
    ativo: bool):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE empresa
          SET
            nome = %s,
            cnpj = %s,
            ativo = %s
            WHERE id = %s
          """,
          (nome,
           cnpj,
           ativo,
           id_empresa))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(id_empresa: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM empresa
          WHERE id = %s
          """,
          (id_empresa,))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_nome_parcial(nome: str):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            id, nome, cnpj, ativo
          FROM empresa
          WHERE
            UPPER(nome)
            LIKE UPPER(%s)
          ORDER BY nome
          LIMIT 10
          """,
          (f"%{nome}%",))

        return cursor.fetchall()

    finally:

      conn.close()

  @staticmethod
  def buscar_por_nome(nome: str, conn=None):
  
    conn_externa = (conn is not None)
    if not conn_externa:
      conn = get_connection()

    try:
      with conn.cursor() as cursor:

        cursor.execute(
          """SELECT id, nome, cnpj, ativo FROM empresa 
          WHERE UPPER(nome) = UPPER(%s)""", (nome,))
  
        return cursor.fetchone()
  
    finally:
      if not conn_externa:
        conn.close()
