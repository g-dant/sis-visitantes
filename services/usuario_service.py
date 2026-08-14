from passlib.hash import bcrypt

from repositories.usuario_repository import UsuarioRepository


class UsuarioService:

  @staticmethod
  def listar():
    return UsuarioRepository.listar()


  @staticmethod
  def buscar_por_id(id_usuario: int):
      return UsuarioRepository.buscar_por_id(id_usuario)


  @staticmethod
  def criar(
    nome: str,
    email: str,
    telefone: str,
    id_tipo: int,
    id_setor: int,
    id_credencial: int,
    senha: str):

    if senha is None:
      raise ValueError("Senha é obrigatória.")

    return UsuarioRepository.inserir(
      nome=nome,
      email=UsuarioService.validar_email_unico(email),
      telefone=telefone,
      id_tipo=id_tipo,
      id_setor=id_setor,
      id_credencial=id_credencial,
      senha_hash=UsuarioService.validar_e_gerar_hash(senha))


  @staticmethod
  def atualizar_tudo(
    id_usuario: int,
    nome: str,
    email: str,
    telefone: str,
    id_tipo: int,
    id_setor: int,
    id_credencial: int,
    senha: str=None,
    ativo: bool=True):

    return UsuarioRepository.atualizar_tudo(
      id_usuario=id_usuario,
      nome=nome,
      email=UsuarioService.validar_email_unico(email, id_usuario),
      telefone=telefone,
      id_tipo=id_tipo,
      id_setor=id_setor,
      id_credencial=id_credencial,
      senha_hash=UsuarioService.validar_e_gerar_hash(senha),
      ativo=ativo)


  @staticmethod
  def excluir(id_usuario: int):
    return UsuarioRepository.excluir(id_usuario)


  @staticmethod
  def atualizar_usuario_logado(
    id_usuario: int,
    email: str | None,
    senha: str | None):
  
    usuario = UsuarioRepository.buscar_por_id(id_usuario)
    if usuario is None:
      raise ValueError("Usuário não encontrado.")
  
    UsuarioRepository.atualizar_usuario_logado(
      id_usuario=id_usuario,
      email=UsuarioService.validar_email_unico(email, id_usuario),
      senha_hash=UsuarioService.validar_e_gerar_hash(senha))


  @staticmethod
  def validar_e_gerar_hash(senha):
  
    if senha is None:
      return
  
    senha = senha.strip()
  
    if senha == "":
      raise ValueError("Senha é obrigatória.")
    
    if len(senha) < 8:
      raise ValueError(
        "A senha deve possuir ao menos 8 caracteres.")
  
    return bcrypt.hash(senha)

  @staticmethod
  def validar_email_unico(email: str, id_usuario: int | None = None):
  
    if email is None:
      raise ValueError("E-mail é obrigatório.")
  
    email = email.strip()
    usuario = UsuarioRepository.buscar_por_email(email)
  
    if usuario:
      if (id_usuario is None or usuario["id"] != id_usuario):
        raise ValueError("E-mail já cadastrado.")
  
    return email

