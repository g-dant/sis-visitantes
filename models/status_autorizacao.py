from pydantic import BaseModel

class StatusAutorizacao(BaseModel):

  id: int | None = None
  nome: str
  descricao: str | None = None
  ativo: bool = True
