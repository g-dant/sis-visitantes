from dataclasses import fields
from models.autorizacao_importacao import AutorizacaoImportacao


class ImportacaoUtils:

  @staticmethod
  def linha_vazia(autorizacao):

    campos = [
      autorizacao.cpf,
      autorizacao.nome,
      autorizacao.empresa,
      autorizacao.placa,
      autorizacao.primeiro_dia,
      autorizacao.ultimo_dia
    ]

    for campo in campos:

      if campo is None:
        continue

      if str(campo).strip():
        return False

    return True
