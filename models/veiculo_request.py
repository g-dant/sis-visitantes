from pydantic import BaseModel


class VeiculoRequest(BaseModel):

  placa: str
  cor: str | None = None
  marca: str | None = None
  tipo: str | None = None
  observacoes: str | None = None
  ativo: bool = True
