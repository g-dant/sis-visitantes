from config.database import get_connection


class AutorizacaoRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:
      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT
            id,
            id_visitante,
            visitante_nome,
            id_status_autorizacao_anterior,
            id_status_autorizacao,
            status_nome,
            status_exibicao,
            id_setor_solicitante,
            setor_solicitante_codigo,
            setor_solicitante_descricao,
            solicitante_nome,
            primeiro_dia,
            ultimo_dia,
            id_veiculo,
            placa,
            marca,
            tipo,
            cor
          FROM autorizacao_consulta
          ORDER BY
            id DESC""")

        return cursor.fetchall()

    finally:
      conn.close()

  @staticmethod
  def buscar_por_id(id_autorizacao: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
            SELECT

            id,
            id_visitante,

            visitante_nome,
            cpf,
            rg,
            email,
            celular,

            id_empresa,
            empresa_nome,

            id_status_autorizacao_anterior,
            id_status_autorizacao,
            status_nome,
            status_exibicao,

            id_setor_solicitante,
            setor_solicitante_codigo,
            setor_solicitante_descricao,

            solicitante_nome,

            primeiro_dia,
            ultimo_dia,

            id_veiculo,

            placa,
            marca,
            tipo,
            cor

          FROM autorizacao_consulta

          WHERE id = %s""",
          (id_autorizacao,))

        return cursor.fetchone()

    finally:
      conn.close()

  @staticmethod
  def inserir(
    id_visitante: int,
    id_empresa: int,
    id_status_autorizacao: int,
    id_setor_solicitante: int,
    id_veiculo: int | None,
    primeiro_dia,
    ultimo_dia,
    conn=None):

    conn_externa = conn is not None
    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO autorizacao (
            id_visitante,
            id_empresa,
            id_status_autorizacao,
            id_setor_solicitante,
            id_veiculo,
            primeiro_dia,
            ultimo_dia)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
          RETURNING id""",
          ( id_visitante,
            id_empresa,
            id_status_autorizacao,
            id_setor_solicitante,
            id_veiculo,
            primeiro_dia,
            ultimo_dia)
        )

        id_autorizacao = cursor.fetchone()["id"]

        if not conn_externa:
          conn.commit()

        return id_autorizacao

    finally:
      if not conn_externa:
        conn.close()


  @staticmethod
  def atualizar_tudo(
    id_autorizacao: int,
    id_visitante: int,
    id_empresa: int,
    id_status_autorizacao_anterior: int | None,
    id_status_autorizacao: int,
    id_setor_solicitante: int,
    id_veiculo: int | None,
    primeiro_dia,
    ultimo_dia):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE autorizacao
          SET
            id_visitante = %s,
            id_empresa = %s,
            id_status_autorizacao_anterior = %s,
            id_status_autorizacao = %s,
            id_setor_solicitante = %s,
            id_veiculo = %s,
            primeiro_dia = %s,
            ultimo_dia = %s
          WHERE id = %s
          """,
          (id_visitante,
           id_empresa,
           id_status_autorizacao_anterior,
           id_status_autorizacao,
           id_setor_solicitante,
           id_veiculo,
           primeiro_dia,
           ultimo_dia,
           id_autorizacao)
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(id_autorizacao: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """DELETE FROM autorizacao
             WHERE id = %s""",
          (id_autorizacao,))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def atualizar_status(
    id_autorizacao: int, 
    id_status_autorizacao_anterior: int | None, 
    id_status_autorizacao: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          UPDATE autorizacao
          SET id_status_autorizacao_anterior = %s, 
          id_status_autorizacao = %s
          WHERE id = %s""",
          (id_status_autorizacao_anterior, 
           id_status_autorizacao, 
           id_autorizacao))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def listar_status_exibicao():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
      SELECT DISTINCT
      status_exibicao
      FROM autorizacao_consulta
      ORDER BY status_exibicao""")

    lista = cur.fetchall()

    cur.close()
    conn.close()

    return lista


  @staticmethod
  def buscar_colisao(
    cpf: str, primeiro_dia, ultimo_dia, id_autorizacao_ignorada: int | None = None):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
        SELECT
          a.id,
          a.primeiro_dia,
          a.ultimo_dia

        FROM autorizacao a

        JOIN visitante v
          ON v.id = a.id_visitante

        JOIN status_autorizacao sa
          ON sa.id = a.id_status_autorizacao

        WHERE
          v.cpf = %s
          AND sa.participa_colisao = true
          AND a.primeiro_dia <= %s
          AND a.ultimo_dia >= %s
          AND (
            %s IS NULL
            OR a.id <> %s
          )

        LIMIT 1
        """, (cpf, ultimo_dia, primeiro_dia,
              id_autorizacao_ignorada,
              id_autorizacao_ignorada))

        return cursor.fetchone()

    finally:
      conn.close()
