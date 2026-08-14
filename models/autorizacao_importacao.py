from dataclasses import dataclass


@dataclass
class AutorizacaoImportacao:

  cpf: str | None = None
  rg: str | None = None
  nome: str | None = None
  email: str | None = None
  celular: str | None = None
  empresa: str | None = None
  placa: str | None = None
  marca: str | None = None
  tipo: str | None = None
  cor: str | None = None
  primeiro_dia: str | None = None
  ultimo_dia: str | None = None

  @staticmethod
  def from_dict(dados: dict):
    return AutorizacaoImportacao(
      cpf=dados["cpf"],
      rg=dados["rg"],
      nome=dados["nome"],
      email=dados["email"],
      celular=dados["celular"],
      empresa=dados["empresa"],
      placa=dados["placa"],
      marca=dados["marca"],
      tipo=dados["tipo"],
      cor=dados["cor"],
      primeiro_dia=dados["primeiro_dia"],
      ultimo_dia=dados["ultimo_dia"])
