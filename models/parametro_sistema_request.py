from pydantic import BaseModel


class ParametroSistemaRequest(BaseModel):

  chave: str
  valor: str
