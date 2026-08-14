from config.database import get_connection


class VisitanteVeiculoRepository:

  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            vv.id,

            vv.id_visitante,
            v.nome AS visitante_nome,

            vv.id_veiculo,
            ve.placa,
            ve.marca,
            ve.tipo

          FROM visitante_veiculo vv

          JOIN visitante v
            ON v.id = vv.id_visitante

          JOIN veiculo ve
            ON ve.id = vv.id_veiculo

          ORDER BY vv.id
          """
        )

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_relacao: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            vv.id,

            vv.id_visitante,
            v.nome AS visitante_nome,

            vv.id_veiculo,
            ve.placa,
            ve.marca,
            ve.tipo

          FROM visitante_veiculo vv

          JOIN visitante v
            ON v.id = vv.id_visitante

          JOIN veiculo ve
            ON ve.id = vv.id_veiculo

          WHERE vv.id = %s
          """,
          (id_relacao,)
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    id_visitante: int,
    id_veiculo: int,
    conn=None
  ):

    conn_externa = conn is not None
    if not conn_externa:
      conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          INSERT INTO visitante_veiculo (
            id_visitante,
            id_veiculo
          )
          VALUES (
            %s,
            %s
          )
          RETURNING id
          """,
          (
            id_visitante,
            id_veiculo
          )
        )

        id_relacao = cursor.fetchone()["id"]

        if not conn_externa:
          conn.commit()

        return id_relacao

    finally:
      if not conn_externa:
        conn.close()


  @staticmethod
  def atualizar_tudo(
    id_relacao: int,
    id_visitante: int,
    id_veiculo: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          UPDATE visitante_veiculo
          SET
            id_visitante = %s,
            id_veiculo = %s
          WHERE id = %s
          """,
          (
            id_visitante,
            id_veiculo,
            id_relacao
          )
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(
    id_relacao: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          DELETE FROM visitante_veiculo
          WHERE id = %s
          """,
          (id_relacao,)
        )

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_visitante_e_veiculo(
    id_visitante: int,
    id_veiculo: int
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            vv.id,

            vv.id_visitante,
            vv.id_veiculo

          FROM visitante_veiculo vv

          WHERE
            vv.id_visitante = %s
            AND vv.id_veiculo = %s
          """,
          (
            id_visitante,
            id_veiculo
          )
        )

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def buscar_veiculo_por_visitante_e_placa(
    id_visitante: int,
    placa: str
  ):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            ve.id,
            ve.placa,
            ve.cor,
            ve.marca,
            ve.tipo,
            ve.observacoes,
            ve.ativo

          FROM visitante_veiculo vv

          JOIN veiculo ve
            ON ve.id = vv.id_veiculo

          WHERE
            vv.id_visitante = %s
            AND UPPER(ve.placa) = UPPER(%s)
          """,
          (
            id_visitante,
            placa
          )
        )

        return cursor.fetchone()

    finally:
      conn.close()

