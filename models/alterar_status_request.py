from pydantic import BaseModel

class AlterarStatusRequest(BaseModel):

  id_status_autorizacao: int
