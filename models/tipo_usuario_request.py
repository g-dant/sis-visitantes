from pydantic import BaseModel


class TipoUsuarioRequest(BaseModel):

  nome: str
  ativo: bool = True
