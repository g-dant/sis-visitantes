from pydantic import BaseModel


class StatusAutorizacaoRequest(BaseModel):

  nome: str
  descricao: str | None = None
  ativo: bool = True
