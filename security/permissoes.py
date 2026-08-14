from config.menu import MENU

from fastapi import Depends, HTTPException, Request

from security.auth_guard import usuario_logado
from services.permissao_service import PermissaoService


def exigir_permissao(codigo_permissao: str):

  def dependencia(sessao=Depends(usuario_logado)):

    permitido = PermissaoService.credencial_possui_permissao(
      id_credencial=sessao["id_credencial"],
      codigo_permissao=codigo_permissao)

    if not permitido:
      raise HTTPException(status_code=403, detail="Acesso negado.")

    return sessao

  return dependencia


def possui_permissao(usuario, codigo_permissao: str):

  if usuario is None:
    return False

  return codigo_permissao in usuario["permissoes"]


def exibir_item_menu(request: Request, usuario, item_menu):

  if usuario is None:
    return False

  if request.url.path == item_menu["url"]:
    return False

  return (
      item_menu["permissao"]
      in usuario["permissoes"])
