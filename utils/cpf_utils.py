import re


class CpfUtils:

  @staticmethod
  def limpar(cpf: str | None):
    if cpf is None:
      return ""

    return re.sub(r"\D", "", cpf)


  @staticmethod
  def validar(cpf: str):
    return len(cpf) == 11
