from pydantic import BaseModel


class LocalRequest(BaseModel):

  codigo: str
  descricao: str
  ativo: bool = True
