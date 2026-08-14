from datetime import date

from pydantic import BaseModel


class EmissaoAutorizacaoDTO(BaseModel):

  cpf: str
  rg: str | None = None

  nome: str
  email: str | None = None
  celular: str | None = None

  empresa_nome: str
  empresa_cnpj: str | None = None

  placa: str | None = None
  marca: str | None = None
  cor: str | None = None
  tipo: str | None = None
  observacoes_veiculo: str | None = None

  primeiro_dia: date
  ultimo_dia: date
