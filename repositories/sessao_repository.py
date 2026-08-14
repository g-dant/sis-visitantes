from config.database import get_connection


class SessaoRepository:

  @staticmethod
  def criar(id_usuario, token, data_inicio, data_expiracao):

    conn = get_connection()

    try:
      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO sessao (
            id_usuario,
            token,
            data_inicio,
            data_expiracao)
          VALUES (%s, %s, %s, %s)
          RETURNING id
          """, (
            id_usuario,
            token,
            data_inicio,
            data_expiracao))

        resultado = cursor.fetchone()
        conn.commit()

        return resultado["id"]
   
    finally:
      conn.close()   


  @staticmethod
  def buscar_por_token(token):

    conn = get_connection()

    try:
      with conn.cursor() as cursor:
        cursor.execute(
          """
          SELECT
            id,
            id_usuario,
            token,
            data_inicio,
            data_expiracao
          FROM sessao
          WHERE token = %s
          """,
          (token,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def buscar_sessao_ativa(token):

    conn = get_connection()

    try:
      with conn.cursor() as cursor:
        cursor.execute("""
          SELECT
            s.id,
            s.id_usuario,
            s.token,
            s.data_inicio,
            s.data_expiracao,
          
            u.nome,
            u.email,
            u.id_credencial,
            u.id_setor,
            u.ativo,
          
            c.nome AS credencial,
          
            se.codigo AS setor_codigo,
            se.descricao AS setor_descricao,
          
            l.descricao AS local_descricao
          
          FROM sessao s
          
          JOIN usuario u
            ON u.id = s.id_usuario
          
          JOIN credencial c
            ON c.id = u.id_credencial
          
          JOIN setor se
            ON se.id = u.id_setor
          
          JOIN local l
            ON l.id = se.id_local
          
          WHERE s.token = %s
          """, (token,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def encerrar(token):
  
    conn = get_connection()
  
    try:
      with conn.cursor() as cursor:
  
        cursor.execute("""
          DELETE FROM sessao
          WHERE token = %s
          """, (token,))
  
        conn.commit()
  
    finally:
      conn.close()
