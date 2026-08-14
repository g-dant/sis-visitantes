from models.autorizacao_importacao import AutorizacaoImportacao
from utils.data_utils import DataUtils
from utils.importacao_utils import ImportacaoUtils


class NormalizadorImportacaoService:

  @staticmethod
  def normalizar(registros):

    resultado = []

    for registro in registros:

      autorizacao = AutorizacaoImportacao(

          cpf=NormalizadorImportacaoService.obter_valor(
            registro, "CPF"),
      
          nome=NormalizadorImportacaoService.obter_valor(
            registro, "Nome"),
      
          empresa=NormalizadorImportacaoService.obter_valor(
            registro, "Empresa"),
      
          placa=NormalizadorImportacaoService.obter_valor(
            registro, "Placa"),
      
          primeiro_dia=DataUtils.parse(
            NormalizadorImportacaoService.obter_valor(
              registro, "Primeiro Dia", "De")),
      
          ultimo_dia=DataUtils.parse(
            NormalizadorImportacaoService.obter_valor(
              registro, "Último Dia", "Até"))
      )

      if ImportacaoUtils.linha_vazia(autorizacao):
        continue

      resultado.append(autorizacao)

    return resultado

  @staticmethod
  def obter_valor(registro: dict, *nomes):

    for nome in nomes:
      valor = registro.get(nome)
      if valor not in (None, ""):
        return valor

    return None

