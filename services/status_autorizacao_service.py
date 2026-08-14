from repositories.status_autorizacao_repository import (
  StatusAutorizacaoRepository
)


class StatusAutorizacaoService:

  @staticmethod
  def listar():

    return StatusAutorizacaoRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_status: int
  ):

    return StatusAutorizacaoRepository.buscar_por_id(
      id_status
    )


  @staticmethod
  def criar(
    nome: str,
    descricao: str | None,
    ativo: bool
  ):

    return StatusAutorizacaoRepository.inserir(
      nome=nome,
      descricao=descricao,
      ativo=ativo
    )


  @staticmethod
  def atualizar_tudo(
    id_status: int,
    nome: str,
    descricao: str | None,
    ativo: bool
  ):

    return StatusAutorizacaoRepository.atualizar_tudo(
      id_status=id_status,
      nome=nome,
      descricao=descricao,
      ativo=ativo
    )


  @staticmethod
  def excluir(
    id_status: int
  ):

    return StatusAutorizacaoRepository.excluir(
      id_status
    )
