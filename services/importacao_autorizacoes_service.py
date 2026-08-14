from models.resultado_importacao import ResultadoImportacao

from services.importadores.csv_importador import CsvImportador
from services.importadores.xlsx_importador import XlsxImportador
from services.importadores.ods_importador import OdsImportador
from services.normalizador_importacao_service import NormalizadorImportacaoService
from services.validacao_importacao_service import ValidacaoImportacaoService

from dataclasses import asdict


class ImportacaoAutorizacoesService:

  @staticmethod
  def importar(arquivo):

    nome = arquivo.filename.lower()
    conteudo = arquivo.file.read()

    if nome.endswith(".csv"):
      registros = CsvImportador.importar(conteudo)

    elif nome.endswith(".xlsx"):
      registros = XlsxImportador.importar(conteudo)

    elif nome.endswith(".ods"):
      registros = OdsImportador.importar(conteudo)

    else:
      return ResultadoImportacao(
        sucesso=False,
        mensagem="Erro no processamento do arquivo.",
        registros=resultados)

    autorizacoes = NormalizadorImportacaoService.normalizar(registros)
    resultado = ValidacaoImportacaoService.validar(autorizacoes)

    resultado.mensagem = ("Arquivo processado com sucesso.")

    return resultado
