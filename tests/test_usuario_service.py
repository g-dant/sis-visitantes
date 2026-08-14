from services.usuario_service import UsuarioService


usuarios = UsuarioService.listar()
print("Quantidade de usuários:", len(usuarios))

print("---\nListagem de usuários")
for usuario in usuarios:
  print(usuario)

print("Criação de usuário via service")
id_usuario = UsuarioService.criar(
  nome="Teste Service",
  email="teste.service@empresa.com",
  telefone="21999999999",
  id_tipo=1,
  id_setor=1,
  id_credencial=1,
  senha="123456"
)

print(id_usuario)

print("Atualização total de usuário")
UsuarioService.atualizar_tudo(
  id_usuario=1,
  nome="Guilherme Vieira Dantas",
  email="vieira.dantas@marinha.mil.br",
  telefone="998864785",
  id_tipo=1,
  id_setor=1,
  id_credencial=1
)

print(UsuarioService.buscar_por_id(1))
