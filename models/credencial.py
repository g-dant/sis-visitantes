from pydantic import BaseModel

class Credencial(BaseModel):

  id: int | None = None
  nome: str
  ativo: bool = True
