import os
import tempfile

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P


class OdsImportador:

  @staticmethod
  def importar(conteudo: bytes):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ods") as temp:
      temp.write(conteudo)
      caminho = temp.name
    try:
      documento = load(caminho)
    finally:
      os.remove(caminho)

    tabela = documento.spreadsheet.getElementsByType(Table)[0]
    linhas = []

    for linha in tabela.getElementsByType(TableRow):

      valores = []
      for celula in linha.getElementsByType(TableCell):

        texto = ""
        paragrafos = celula.getElementsByType(P)

        if paragrafos:

          texto = "".join(
            p.firstChild.data if p.firstChild else ""
            for p in paragrafos
          )

        valores.append(texto)

      linhas.append(valores)

    if not linhas:
      return []

    cabecalho = linhas[0]
    registros = []

    for linha in linhas[1:]:

      registro = {}

      for coluna, valor in zip(cabecalho, linha):
        registro[coluna] = valor

      registros.append(registro)

    return registros
