from config.app_config import NOME_SISTEMA, DESCRICAO_SISTEMA
from config.menu import MENU

from fastapi import Request

from security.token_extractor import TokenExtractor
from services.sessao_service import SessaoService


class TemplateContextService:

  @staticmethod
  def criar(request: Request, **extras):

    token = TokenExtractor.extrair(request)
    usuario = None

    if token is not None:
      sessao = SessaoService.obter_sessao_por_token(token)

      if sessao is not None:
        usuario = SessaoService.obter_contexto(sessao)

    contexto = {

      "nome_sistema": NOME_SISTEMA,
      "descricao_sistema": DESCRICAO_SISTEMA,

      "menu": MENU,

      "usuario": usuario }

    contexto.update(extras)
    return contexto
