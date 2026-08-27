from pydantic import BaseModel


class CredencialAtualizacaoRequest(BaseModel):

  nome: str
  descricao: str | None = None
