from getpass import getpass
from services.auth_service import (AuthService)

email = input("E-mail: ")
senha = getpass("Senha: ")

usuario = (AuthService.autenticar(email, senha))

if usuario is None:
  print("\nFalha na autenticação.")

else:
  print("\nAutenticação realizada com sucesso.")
  print(f"Usuário: {usuario['nome']}")
  print(f"Credencial: {usuario['credencial_nome']}")
  print(f"Local: {usuario['local_codigo']}")
  print(f"Setor: {usuario['setor_codigo']}")
