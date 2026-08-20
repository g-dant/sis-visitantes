from config.database import get_connection


class VisitanteRepository:

  @staticmethod
  def listar():
  
    conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          SELECT
            v.id,
            v.nome,
            v.email,
            v.celular,
            v.rg,
            v.cpf,
            v.ativo,

            v.id_empresa,
            e.nome AS empresa_nome,
            e.cnpj AS empresa_cnpj,
  
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM autorizacao a
                WHERE a.id_visitante = v.id)
              THEN false
              ELSE true
            END AS pode_excluir
  
          FROM visitante v
  
          JOIN empresa e
            ON e.id = v.id_empresa
  
          ORDER BY v.nome
          """)
  
        return cursor.fetchall()
  
    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_visitante: int):
  
    conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          SELECT
            v.id,
            v.nome,
            v.email,
            v.celular,
            v.rg,
            v.cpf,
            v.ativo,
  
            v.id_empresa,
            e.nome AS empresa_nome,
            e.cnpj AS empresa_cnpj,
  
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM autorizacao a
                WHERE a.id_visitante = v.id
              )
              THEN false
              ELSE true
            END AS pode_excluir
  
          FROM visitante v
  
          JOIN empresa e
            ON e.id = v.id_empresa
  
          WHERE v.id = %s""",
          (id_visitante,))
  
        return cursor.fetchone()
  
    finally:
      conn.close()


  @staticmethod
  def inserir(nome, email, celular, rg, cpf, id_empresa, ativo, conn=None):
    
    conn_externa = conn is not None

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO visitante (
            nome,
            email,
            celular,
            rg,
            cpf,
            id_empresa,
            ativo)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
          RETURNING id
          """,
          (nome,
           email,
           celular,
           rg,
           cpf,
           id_empresa,
           ativo))

        id_visitante = cursor.fetchone()["id"]

        if not conn_externa:
          conn.commit()

        return id_visitante

    finally:
      if not conn_externa:
        conn.close()


  @staticmethod
  def atualizar_tudo(
    id_visitante,
    nome,
    email,
    celular,
    rg,
    cpf,
    id_empresa,
    ativo):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE visitante
          SET
            nome = %s,
            email = %s,
            celular = %s,
            rg = %s,
            cpf = %s,
            id_empresa = %s,
            ativo = %s
          WHERE id = %s
          """,
          (nome, email, celular, rg, cpf, id_empresa, ativo, id_visitante))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(id_visitante: int, conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM visitante
          WHERE id = %s""", (id_visitante,))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()


  @staticmethod
  def buscar_por_cpf(cpf: str, conn=None):
  
    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          SELECT
            v.id,
            v.nome,
            v.email,
            v.celular,
            v.rg,
            v.cpf,
            v.id_empresa,
            e.nome AS empresa_nome,
            v.ativo
  
          FROM visitante v
  
          LEFT JOIN empresa e
            ON e.id = v.id_empresa
  
          WHERE v.cpf = %s
          """, (cpf,))
  
        return cursor.fetchone()
  
    finally:
      if not conn_externa:
        conn.close()

  @staticmethod
  def atualizar_empresa(
    id_visitante: int,
    id_empresa: int,
    conn=None):
  
    conn_externa = (conn is not None)
  
    if not conn_externa:
      conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          UPDATE visitante
          SET id_empresa = %s
          WHERE id = %s
          """, (id_empresa, id_visitante))
  
      if not conn_externa:
        conn.commit()
  
    finally:
  
      if not conn_externa:
        conn.close()

  @staticmethod
  def existe_autorizacao(id_visitante: int, conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT 1
          FROM autorizacao
          WHERE id_visitante = %s
          LIMIT 1
          """, (id_visitante,))

        return cursor.fetchone() is not None

    finally:

      if not conn_externa:
        conn.close()

  @staticmethod
  def excluir_associacoes_veiculo(
    id_visitante: int,
    conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM visitante_veiculo
          WHERE id_visitante = %s
          """, (id_visitante,))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()


