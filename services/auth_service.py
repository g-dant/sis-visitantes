from passlib.hash import bcrypt
from repositories.usuario_repository import (UsuarioRepository)


class AuthService:

  @staticmethod
  def autenticar(email: str, senha: str):

    usuario = (UsuarioRepository.buscar_por_email(email))

    if usuario is None:
      return None

    if not usuario["ativo"]:
      return None

    senha_valida = bcrypt.verify(senha, usuario["senha_hash"])

    if not senha_valida:
      return None

    return usuario
