from config.database import get_connection


class VeiculoRepository:

  @staticmethod
  def listar():
  
    conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
          
        cursor.execute("""
          SELECT
            v.id,
            v.placa,
            v.cor,
            v.marca,
            v.tipo,
            v.observacoes,
            v.ativo,
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM visitante_veiculo vv
                WHERE vv.id_veiculo = v.id
              )
              OR EXISTS (
                SELECT 1
                FROM autorizacao a
                WHERE a.id_veiculo = v.id
              )
              THEN false
              ELSE true
            END AS pode_excluir
          FROM veiculo v
          ORDER BY v.placa
          """)
  
        return cursor.fetchall()
  
    finally:
      conn.close()

  @staticmethod
  def buscar_por_id(id_veiculo: int):
  
    conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          SELECT
            v.id,
            v.placa,
            v.cor,
            v.marca,
            v.tipo,
            v.observacoes,
            v.ativo,
            CASE
              WHEN EXISTS (
                SELECT 1
                FROM visitante_veiculo vv
                WHERE vv.id_veiculo = v.id)
              THEN false
              ELSE true
            END AS pode_excluir
          FROM veiculo v
          WHERE v.id = %s
          """, (id_veiculo,))
  
        return cursor.fetchone()
  
    finally:
      conn.close()

  @staticmethod
  def inserir(
    placa: str,
    cor: str | None,
    marca: str | None,
    tipo: str | None,
    observacoes: str | None,
    ativo: bool,
    conn=None):

    conn_externa = conn is not None
    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO veiculo (
            placa,
            cor,
            marca,
            tipo,
            observacoes,
            ativo)
          VALUES (
            %s, %s, %s, %s, %s, %s)
          RETURNING id
          """, (
            placa,
            cor,
            marca,
            tipo,
            observacoes,
            ativo))

        id_veiculo = cursor.fetchone()["id"]

        if not conn_externa:
          conn.commit()

        return id_veiculo

    finally:

      if not conn_externa:
        conn.close()

  @staticmethod
  def atualizar_tudo(
    id_veiculo: int,
    placa: str,
    cor: str | None,
    marca: str | None,
    tipo: str | None,
    observacoes: str | None,
    ativo: bool):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE veiculo
          SET
            placa = %s,
            cor = %s,
            marca = %s,
            tipo = %s,
            observacoes = %s,
            ativo = %s
          WHERE id = %s
          """, (
            placa,
            cor,
            marca,
            tipo,
            observacoes,
            ativo,
            id_veiculo))

        conn.commit()

    finally:
      conn.close()

  @staticmethod
  def excluir(id_veiculo: int, conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM veiculo WHERE id = %s""",
          (id_veiculo,))

      if not conn_externa:
        conn.commit()

    finally:

      if not conn_externa:
        conn.close()

  @staticmethod
  def buscar_por_placa(placa: str, conn=None):
  
    conn_externa = (conn is not None)
    if not conn_externa:
      conn = get_connection()
  
    try:
  
      with conn.cursor() as cursor:
  
        cursor.execute("""
          SELECT
            id,
            placa,
            cor,
            marca,
            tipo,
            observacoes,
            ativo
          FROM veiculo
          WHERE UPPER(placa) = UPPER(%s)""", (placa,))
  
        return cursor.fetchone()
  
    finally:
      if not conn_externa:
        conn.close()

  @staticmethod
  def existe_associacao_visitante(
    id_veiculo: int,
    conn=None):

    conn_externa = (conn is not None)

    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT 1
          FROM visitante_veiculo
          WHERE id_veiculo = %s
          LIMIT 1
          """, (id_veiculo,))

        return cursor.fetchone() is not None

    finally:

      if not conn_externa:
        conn.close()
