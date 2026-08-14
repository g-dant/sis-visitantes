from repositories.usuario_repository import UsuarioRepository

usuarios = UsuarioRepository.listar()

print(len(usuarios))
print(usuarios[0])
