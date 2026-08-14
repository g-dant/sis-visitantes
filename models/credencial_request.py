from pydantic import BaseModel


class CredencialRequest(BaseModel):

  nome: str
  ativo: bool = True
