from pydantic import BaseModel


class UsuarioAtualizacao(BaseModel):

  email: str | None = None
  senha: str | None = None
