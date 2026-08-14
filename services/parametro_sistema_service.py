from repositories.parametro_sistema_repository import ParametroSistemaRepository


class ParametroSistemaService:

  @staticmethod
  def listar():
    return ParametroSistemaRepository.listar()


  @staticmethod
  def buscar_por_id(id_parametro_sistema: int):
    return ParametroSistemaRepository.buscar_por_id(
        id_parametro_sistema)
    

  @staticmethod
  def criar(chave: str, valor: str):
    return ParametroSistemaRepository.inserir(chave=chave, valor=valor)


  @staticmethod
  def atualizar_tudo(
    id_parametro_sistema: int,
    chave: str,
    valor: str
  ):

    ParametroSistemaRepository.atualizar_tudo(
      id_parametro_sistema=id_parametro_sistema,
      chave=chave,
      valor=valor
    )


  @staticmethod
  def excluir(id_parametro_sistema: int):
    ParametroSistemaRepository.excluir(id_parametro_sistema)


  @staticmethod
  def obter(chave: str):

    parametro = ParametroSistemaRepository.buscar_por_chave(chave)
    if parametro is None:
      raise Exception(f"Parâmetro inexistente: {chave}")

    return parametro["valor"]


  @staticmethod
  def obter_int(chave: str):
    return int(ParametroSistemaService.obter(chave))


  @staticmethod
  def obter_bool(chave: str):
    return (ParametroSistemaService
      .obter(chave).lower() == "true")
