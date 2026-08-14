from repositories.tipo_usuario_repository import (
  TipoUsuarioRepository
)


class TipoUsuarioService:

  @staticmethod
  def listar():

    return TipoUsuarioRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_tipo: int
  ):

    return TipoUsuarioRepository.buscar_por_id(
      id_tipo
    )


  @staticmethod
  def criar(
    nome: str,
    ativo: bool
  ):

    return TipoUsuarioRepository.inserir(
      nome=nome,
      ativo=ativo
    )


  @staticmethod
  def atualizar_tudo(
    id_tipo: int,
    nome: str,
    ativo: bool
  ):

    return TipoUsuarioRepository.atualizar_tudo(
      id_tipo=id_tipo,
      nome=nome,
      ativo=ativo
    )


  @staticmethod
  def excluir(
    id_tipo: int
  ):

    return TipoUsuarioRepository.excluir(
      id_tipo
    )
