from repositories.local_repository import (
  LocalRepository
)


class LocalService:

  @staticmethod
  def listar():

    return LocalRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_local: int
  ):

    return LocalRepository.buscar_por_id(
      id_local
    )


  @staticmethod
  def criar(
    codigo: str,
    descricao: str,
    ativo: bool
  ):

    return LocalRepository.inserir(
      codigo=codigo,
      descricao=descricao,
      ativo=ativo
    )


  @staticmethod
  def atualizar_tudo(
    id_local: int,
    codigo: str,
    descricao: str,
    ativo: bool
  ):

    return LocalRepository.atualizar_tudo(
      id_local=id_local,
      codigo=codigo,
      descricao=descricao,
      ativo=ativo
    )


  @staticmethod
  def excluir(
    id_local: int
  ):

    return LocalRepository.excluir(
      id_local
    )
