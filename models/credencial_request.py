from pydantic import BaseModel


class CredencialRequest(BaseModel):

  nome: str
  descricao: str | None = None
  ativo: bool = True
  ids_permissoes: list[int] = []
