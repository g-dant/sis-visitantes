from models.usuario import Usuario

usuario = Usuario(
  nome="João",
  email="joao@email.com",
  id_tipo=1,
  id_local=1,
  id_setor=1,
  id_credencial=1,
  senha_hash="abc"
)

print(usuario)
