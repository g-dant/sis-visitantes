from config.database import get_connection

from repositories.credencial_repository import CredencialRepository
from repositories.credencial_permissao_repository import CredencialPermissaoRepository


class CredencialService:

  @staticmethod
  def listar():
    return CredencialRepository.listar()

  @staticmethod
  def buscar_por_id(id_credencial: int):
    return CredencialRepository.buscar_por_id(id_credencial)

  @staticmethod
  def criar(
    nome: str,
    descricao: str | None,
    ativo: bool,
    ids_permissoes: list[int]):

    conn = get_connection()

    try:

      id_credencial = CredencialRepository.inserir(
        nome=nome,
        descricao=descricao,
        ativo=ativo,
        conn=conn)

      for id_permissao in ids_permissoes:

        CredencialPermissaoRepository.inserir(
          id_credencial=id_credencial,
          id_permissao=id_permissao,
          conn=conn)

      conn.commit()
      return id_credencial

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()

  @staticmethod
  def atualizar_tudo(id_credencial: int, nome: str, descricao: str | None, ativo: bool):

    return CredencialRepository.atualizar_tudo(
      id_credencial=id_credencial,
      nome=nome,
      descricao=descricao,
      ativo=ativo)

  @staticmethod
  def habilitar_permissao(
    id_credencial: int,
    id_permissao: int):

    conn = get_connection()

    try:

      CredencialPermissaoRepository.inserir(
        id_credencial=id_credencial,
        id_permissao=id_permissao,
        conn=conn)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()


  @staticmethod
  def desabilitar_permissao(
    id_credencial: int,
    id_permissao: int):

    conn = get_connection()

    try:

      CredencialPermissaoRepository.excluir_por_credencial_e_permissao(
        id_credencial=id_credencial,
        id_permissao=id_permissao,
        conn=conn)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()

  @staticmethod
  def excluir(id_credencial: int):

    conn = get_connection()

    try:

      CredencialPermissaoRepository.excluir_por_credencial(
        id_credencial=id_credencial, conn=conn)

      CredencialRepository.excluir(
        id_credencial=id_credencial, conn=conn)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()
