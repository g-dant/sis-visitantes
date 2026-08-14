from datetime import datetime
from pydantic import BaseModel


class Sessao(BaseModel):

  id: int | None = None
  id_usuario: int
  token: str
  data_inicio: datetime
  data_expiracao: datetime
