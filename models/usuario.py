from datetime import datetime
from pydantic import BaseModel


class Usuario(BaseModel):

  id: int | None = None
  nome: str
  email: str
  telefone: str | None = None
  id_tipo: int
  id_setor: int
  id_credencial: int
  senha_hash: str
  ativo: bool = True
  data_criacao: datetime | None = None
  data_ultima_alteracao: datetime | None = None
