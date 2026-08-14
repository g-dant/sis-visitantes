from dataclasses import dataclass, field

from models.linha_importacao import LinhaImportacao


@dataclass
class ResultadoImportacao:

  sucesso: bool
  mensagem: str
  linhas: list[LinhaImportacao] = field(default_factory=list)
  erros_globais: list[str] = field(default_factory=list)

  @staticmethod
  def from_dict(dados: dict):

    return ResultadoImportacao(

      sucesso=dados["sucesso"],
      mensagem=dados["mensagem"],

      linhas=[ LinhaImportacao.from_dict(linha)
        for linha in dados["linhas"] ],

      erros_globais=dados.get("erros_globais", []))
