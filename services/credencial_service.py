from repositories.credencial_repository import (
  CredencialRepository
)


class CredencialService:

  @staticmethod
  def listar():

    return CredencialRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_credencial: int
  ):

    return CredencialRepository.buscar_por_id(
      id_credencial
    )


  @staticmethod
  def criar(
    nome: str,
    ativo: bool
  ):

    return CredencialRepository.inserir(
      nome=nome,
      ativo=ativo
    )


  @staticmethod
  def atualizar_tudo(
    id_credencial: int,
    nome: str,
    ativo: bool
  ):

    return CredencialRepository.atualizar_tudo(
      id_credencial=id_credencial,
      nome=nome,
      ativo=ativo
    )


  @staticmethod
  def excluir(
    id_credencial: int
  ):

    return CredencialRepository.excluir(
      id_credencial
    )
