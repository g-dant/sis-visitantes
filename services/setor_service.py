from repositories.setor_repository import (
  SetorRepository
)


class SetorService:

  @staticmethod
  def listar():

    return SetorRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_setor: int
  ):

    return SetorRepository.buscar_por_id(
      id_setor
    )


  @staticmethod
  def criar(
    codigo: str,
    descricao: str,
    ativo: bool,
    id_local: int
  ):

    return SetorRepository.inserir(
      codigo=codigo,
      descricao=descricao,
      ativo=ativo,
      id_local=id_local
    )


  @staticmethod
  def atualizar_tudo(
    id_setor: int,
    codigo: str,
    descricao: str,
    ativo: bool,
    id_local: int
  ):

    return SetorRepository.atualizar_tudo(
      id_setor=id_setor,
      codigo=codigo,
      descricao=descricao,
      ativo=ativo,
      id_local=id_local
    )


  @staticmethod
  def excluir(
    id_setor: int
  ):

    return SetorRepository.excluir(
      id_setor
    )
