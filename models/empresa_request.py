from pydantic import BaseModel


class EmpresaRequest(BaseModel):

  nome: str
  cnpj: str
  ativo: bool = True
