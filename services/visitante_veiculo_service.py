from repositories.visitante_veiculo_repository import (
  VisitanteVeiculoRepository
)


class VisitanteVeiculoService:

  @staticmethod
  def listar():

    return VisitanteVeiculoRepository.listar()


  @staticmethod
  def buscar_por_id(
    id_relacao: int
  ):

    return VisitanteVeiculoRepository.buscar_por_id(
      id_relacao
    )


  @staticmethod
  def criar(
    id_visitante: int,
    id_veiculo: int,
    conn=None
  ):

    return VisitanteVeiculoRepository.inserir(
      id_visitante=id_visitante,
      id_veiculo=id_veiculo,
      conn=conn
    )


  @staticmethod
  def atualizar_tudo(
    id_relacao: int,
    id_visitante: int,
    id_veiculo: int
  ):

    return VisitanteVeiculoRepository.atualizar_tudo(
      id_relacao=id_relacao,
      id_visitante=id_visitante,
      id_veiculo=id_veiculo
    )


  @staticmethod
  def excluir(
    id_relacao: int
  ):

    return VisitanteVeiculoRepository.excluir(
      id_relacao
    )


  @staticmethod
  def buscar_por_visitante_e_veiculo(
    id_visitante: int,
    id_veiculo: int
  ):

    return (
      VisitanteVeiculoRepository
      .buscar_por_visitante_e_veiculo(
        id_visitante=id_visitante,
        id_veiculo=id_veiculo
      )
    )


  @staticmethod
  def buscar_veiculo_por_visitante_e_placa(
    id_visitante: int,
    placa: str
  ):

    return (
      VisitanteVeiculoRepository
      .buscar_veiculo_por_visitante_e_placa(
        id_visitante=id_visitante,
        placa=placa
      )
    )
