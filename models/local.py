from pydantic import BaseModel

class Local(BaseModel):

  id: int | None = None
  codigo: str
  descricao: str
  ativo: bool = True
