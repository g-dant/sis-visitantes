from pydantic import BaseModel


class VisitanteVeiculoRequest(BaseModel):

  id_visitante: int
  id_veiculo: int
