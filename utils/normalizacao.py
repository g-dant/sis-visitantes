def somente_digitos(valor):

  if valor is None:
    return None

  return "".join(c for c in valor if c.isdigit())


def somente_alfanumericos(valor):

  if valor is None:
    return None

  return "".join(c for c in valor if c.isalnum())


def somente_alfanumericos_maiusculos(valor):

  alfanumericos = somente_alfanumericos(valor)
  if alfanumericos is None:
    return None

  return alfanumericos.upper()

def normalizar_dto_emissao_autorizacao(dto):

  dto_normalizado = dto.model_copy(deep=True)

  dto_normalizado.cpf = somente_digitos(dto_normalizado.cpf)
  dto_normalizado.rg = somente_alfanumericos(dto_normalizado.rg)
  dto_normalizado.celular = somente_digitos(dto_normalizado.celular)
  dto_normalizado.placa = somente_alfanumericos_maiusculos(dto_normalizado.placa)
  dto_normalizado.empresa_cnpj = somente_digitos(dto_normalizado.empresa_cnpj)

  return dto_normalizado

