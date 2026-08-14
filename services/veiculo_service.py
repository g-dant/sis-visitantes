from repositories.veiculo_repository import VeiculoRepository


class VeiculoService:

  @staticmethod
  def listar():
    return VeiculoRepository.listar()

  @staticmethod
  def buscar_por_id(id_veiculo: int):
    return VeiculoRepository.buscar_por_id(id_veiculo)


  @staticmethod
  def criar(
    placa: str,
    cor: str | None,
    marca: str | None,
    tipo: str | None,
    observacoes: str | None,
    ativo: bool,
    conn=None):

    return VeiculoRepository.inserir(
      placa=placa,
      cor=cor,
      marca=marca,
      tipo=tipo,
      observacoes=observacoes,
      ativo=ativo,
      conn=conn)


  @staticmethod
  def atualizar_tudo(
    id_veiculo: int,
    placa: str,
    cor: str | None,
    marca: str | None,
    tipo: str | None,
    observacoes: str | None,
    ativo: bool):

    return VeiculoRepository.atualizar_tudo(
      id_veiculo=id_veiculo,
      placa=placa,
      cor=cor,
      marca=marca,
      tipo=tipo,
      observacoes=observacoes,
      ativo=ativo)


  @staticmethod
  def excluir(id_veiculo: int):
    return VeiculoRepository.excluir(id_veiculo)

  @staticmethod
  def buscar_por_placa(placa: str):
    return VeiculoRepository.buscar_por_placa(placa)

  @staticmethod
  def obter_ou_criar(placa: str, conn):

    if not placa:
      return None

    veiculo = VeiculoRepository.buscar_por_placa(placa, conn=conn)

    if veiculo:
      return veiculo["id"]

    return VeiculoRepository.inserir(
      placa=placa,
      cor=None,
      marca=None,
      tipo=None,
      observacoes=None,
      ativo=True,
      conn=conn)
