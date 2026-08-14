from datetime import date
from pydantic import BaseModel


class AutorizacaoRequest(BaseModel):

  id_visitante: int
  id_empresa: int

  # Não há id_autorizacao_anterior: o service faz o trabalho de captar o id anterior
  id_status_autorizacao: int
  id_setor_solicitante: int

  id_veiculo: int | None

  primeiro_dia: date
  ultimo_dia: date
