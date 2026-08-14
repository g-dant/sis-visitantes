from config.database import get_connection


class UsuarioRepository:

  @staticmethod
  def buscar_por_email(email: str):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            u.id,
            u.nome,
            u.email,
            u.telefone,

            u.id_tipo,
            t.nome AS tipo_nome,

            u.id_setor,
            s.codigo AS setor_codigo,
            s.descricao AS setor_descricao,

            l.id AS id_local,
            l.codigo AS local_codigo,
            l.descricao AS local_descricao,

            u.id_credencial,
            c.nome AS credencial_nome,

            u.senha_hash,
            u.ativo,
            u.data_criacao,
            u.data_ultima_alteracao

          FROM usuario u

          JOIN tipo_usuario t
            ON t.id = u.id_tipo

          JOIN setor s
            ON s.id = u.id_setor

          JOIN local l
            ON l.id = s.id_local

          JOIN credencial c
            ON c.id = u.id_credencial

          WHERE lower(u.email) = lower(%s)
          """, (email,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def listar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            u.id,
            u.nome,
            u.email,
            u.telefone,

            u.id_tipo,
            t.nome AS tipo_nome,

            u.id_setor,
            s.codigo AS setor_codigo,
            s.descricao AS setor_descricao,

            l.id AS id_local,
            l.codigo AS local_codigo,
            l.descricao AS local_descricao,

            u.id_credencial,
            c.nome AS credencial_nome,

            u.ativo,
            u.data_criacao,
            u.data_ultima_alteracao

          FROM usuario u

          JOIN tipo_usuario t
            ON t.id = u.id_tipo

          JOIN setor s
            ON s.id = u.id_setor

          JOIN local l
            ON l.id = s.id_local

          JOIN credencial c
            ON c.id = u.id_credencial

          ORDER BY u.nome
          """)

        return cursor.fetchall()

    finally:
      conn.close()


  @staticmethod
  def buscar_por_id(id_usuario: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute(
          """
          SELECT
            u.id,
            u.nome,
            u.email,
            u.telefone,

            u.id_tipo,
            t.nome AS tipo_nome,

            u.id_setor,
            s.codigo AS setor_codigo,
            s.descricao AS setor_descricao,

            l.id AS id_local,
            l.codigo AS local_codigo,
            l.descricao AS local_descricao,

            u.id_credencial,
            c.nome AS credencial_nome,

            u.ativo,
            u.data_criacao,
            u.data_ultima_alteracao

          FROM usuario u

          JOIN tipo_usuario t
            ON t.id = u.id_tipo

          JOIN setor s
            ON s.id = u.id_setor

          JOIN local l
            ON l.id = s.id_local

          JOIN credencial c
            ON c.id = u.id_credencial

          WHERE u.id = %s
          """, (id_usuario,))

        return cursor.fetchone()

    finally:
      conn.close()


  @staticmethod
  def inserir(
    nome: str,
    email: str,
    telefone: str,
    id_tipo: int,
    id_setor: int,
    id_credencial: int,
    senha_hash: str):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          INSERT INTO usuario (
            nome,
            email,
            telefone,
            id_tipo,
            id_setor,
            id_credencial,
            senha_hash
          )
          VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s)
          RETURNING id
          """,
          ( nome,
            email,
            telefone,
            id_tipo,
            id_setor,
            id_credencial,
            senha_hash))

        id_usuario = cursor.fetchone()["id"]

        conn.commit()

        return id_usuario

    finally:
      conn.close()


  @staticmethod
  def atualizar_tudo(
    id_usuario: int,
    nome: str,
    email: str,
    telefone: str,
    id_tipo: int,
    id_setor: int,
    id_credencial: int,
    senha_hash: str | None,
    ativo: bool):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        if senha_hash is None:

          cursor.execute("""
            UPDATE usuario
            SET
              nome = %s,
              email = %s,
              telefone = %s,
              id_tipo = %s,
              id_setor = %s,
              id_credencial = %s,
              ativo = %s,
              data_ultima_alteracao = CURRENT_TIMESTAMP
            WHERE id = %s
            """, (
              nome,
              email,
              telefone,
              id_tipo,
              id_setor,
              id_credencial,
              ativo,
              id_usuario))

        else:

          cursor.execute("""
            UPDATE usuario
            SET
              nome = %s,
              email = %s,
              telefone = %s,
              id_tipo = %s,
              id_setor = %s,
              id_credencial = %s,
              senha_hash = %s,
              ativo = %s,
              data_ultima_alteracao = CURRENT_TIMESTAMP
            WHERE id = %s""", (
              nome,
              email,
              telefone,
              id_tipo,
              id_setor,
              id_credencial,
              senha_hash,
              ativo,
              id_usuario))

        conn.commit()

    finally:
      conn.close()


  @staticmethod
  def excluir(id_usuario: int):

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          DELETE FROM usuario
          WHERE id = %s
          """, (id_usuario,))

        conn.commit()

    finally:
      conn.close()

  @staticmethod
  def atualizar_usuario_logado(
    id_usuario: int, email: str | None, senha_hash: str | None):

    conn = get_connection()

    try:

      with conn.cursor() as cur:
        if email is not None:
          cur.execute("""
            UPDATE usuario
            SET email = %s
            WHERE id = %s
            """, (email, id_usuario))

        if senha_hash is not None:
          cur.execute("""
            UPDATE usuario
            SET senha_hash = %s
            WHERE id = %s""", (senha_hash, id_usuario))

      conn.commit()

    finally:
      conn.close()
