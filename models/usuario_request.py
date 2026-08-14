from pydantic import BaseModel


class UsuarioRequest(BaseModel):

  nome: str
  email: str
  telefone: str

  id_tipo: int
  id_setor: int
  id_credencial: int

  senha: str
