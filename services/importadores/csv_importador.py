import csv
import io


class CsvImportador:

  @staticmethod
  def importar(conteudo: bytes):

    texto = conteudo.decode("utf-8")
    leitor = csv.DictReader(io.StringIO(texto))
    return list(leitor)
