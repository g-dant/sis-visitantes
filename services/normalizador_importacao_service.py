from models.autorizacao_importacao import AutorizacaoImportacao

from utils.data_utils import DataUtils
from utils.exceptions import HeaderInvalidoError
from utils.importacao_utils import ImportacaoUtils


class NormalizadorImportacaoService:

  @staticmethod
  def headerValido(registros):
    chaves_esperadas = {"CPF", "NOME", "EMPRESA", "PLACA", "DE", "ATÉ"}
    return all({chave.strip().upper() for chave in item} == chaves_esperadas 
      for item in registros)

  @staticmethod
  def normalizar(registros):

    resultado = []

    # Antes de chamar as colunas, verificar se header é válido
    if not NormalizadorImportacaoService.headerValido(registros):
      raise HeaderInvalidoError("A planilha deve possuir exatamente as colunas: "
        "CPF, NOME, EMPRESA, PLACA, DE e ATÉ")

    # Aqui se iniciam as referências às colunas já validadas
    for registro in registros:

      autorizacao = AutorizacaoImportacao(

          cpf=NormalizadorImportacaoService.obter_valor(
            registro, "CPF"),
      
          nome=NormalizadorImportacaoService.obter_valor(
            registro, "Nome").upper(),
      
          empresa=NormalizadorImportacaoService.obter_valor(
            registro, "Empresa").upper(),
      
          placa=NormalizadorImportacaoService.obter_valor(
            registro, "Placa").upper(),
      
          primeiro_dia=DataUtils.parse(
            NormalizadorImportacaoService.obter_valor(
              registro, "Primeiro Dia", "De")),
      
          ultimo_dia=DataUtils.parse(
            NormalizadorImportacaoService.obter_valor(
              registro, "Último Dia", "Até")))

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

    return ""

