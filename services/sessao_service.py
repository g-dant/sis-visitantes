from fastapi import Request
from repositories.sessao_repository import SessaoRepository
from services.permissao_service import PermissaoService


class SessaoService:

  @staticmethod
  def obter_contexto(sessao):
  
    return {
      "id_usuario": sessao["id_usuario"],
      "nome": sessao["nome"],
      "email": sessao["email"],
  
      "id_credencial": sessao["id_credencial"],
      "credencial": sessao["credencial"],
  
      "setor_codigo": sessao["setor_codigo"],
      "setor_descricao": sessao["setor_descricao"],
  
      "local_descricao": sessao["local_descricao"],
  
      "permissoes": PermissaoService.listar_permissoes(
        sessao["id_credencial"]) }
  
  
  @staticmethod
  def obter_sessao_por_token(token):
  
    return SessaoRepository.buscar_sessao_ativa(token)
  
  
  @staticmethod
  def obter_contexto_por_token(token):
  
    sessao = SessaoRepository.buscar_sessao_ativa(token)
  
    if sessao is None:
      return None
  
    return SessaoService.obter_contexto(sessao)
  
  
  @staticmethod
  def obter_contexto_por_request(request: Request):
  
    authorization = request.headers.get("Authorization")
  
    if authorization is None:
      return None
  
    if not authorization.startswith("Bearer "):
      return None
  
    token = authorization.replace("Bearer ", "")
  
    return SessaoService.obter_contexto_por_token(token)
