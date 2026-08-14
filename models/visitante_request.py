from pydantic import BaseModel


class VisitanteRequest(BaseModel):

  nome: str
  email: str | None = None
  celular: str | None = None
  rg: str | None = None
  cpf: str
  id_empresa: int
  ativo: bool = True
