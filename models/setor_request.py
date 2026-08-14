from pydantic import BaseModel


class SetorRequest(BaseModel):

  codigo: str
  descricao: str
  ativo: bool = True

  id_local: int
