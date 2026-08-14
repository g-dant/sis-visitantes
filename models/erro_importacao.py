from dataclasses import dataclass


@dataclass
class ErroImportacao:

  campo: str
  mensagem: str

  @staticmethod
  def from_dict(dados: dict):
    return ErroImportacao(
      campo=dados["campo"], mensagem=dados["mensagem"])
