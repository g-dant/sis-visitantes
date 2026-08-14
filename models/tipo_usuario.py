from pydantic import BaseModel

class TipoUsuario(BaseModel):

  id: int | None = None
  nome: str
  ativo: bool = True
