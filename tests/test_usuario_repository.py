from repositories.usuario_repository import UsuarioRepository

print("\n---\nTeste de busca por e-mail:")
usuario = UsuarioRepository.buscar_por_email("vieira.dantas@marinha.mil.br")
print(usuario)

print("---\nTeste de inserção:")
id_usuario = UsuarioRepository.inserir(
  nome="Teste",
  email="teste@empresa.com",
  telefone="21999999999",
  id_tipo=1,
  id_setor=1,
  id_credencial=1,
  senha_hash="HASH_TESTE"
)
print('---\n' + str(id_usuario))
