from pydantic import BaseModel

class Setor(BaseModel):

  id: int | None = None
  id_local: int
  codigo: str
  descricao: str
  ativo: bool = True
