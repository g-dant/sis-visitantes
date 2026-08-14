from datetime import datetime

from fastapi import HTTPException, Request

from repositories.sessao_repository import SessaoRepository
from security.token_extractor import TokenExtractor


def usuario_logado(request: Request):

  token = TokenExtractor.extrair(request)

  if token is None:
    raise HTTPException(status_code=401, detail="Token não informado")

  sessao = (SessaoRepository.buscar_sessao_ativa(token))
  if sessao is None:
    raise HTTPException(status_code=401, detail="Sessão inexistente")

  if not sessao["ativo"]:
    raise HTTPException(status_code=401, detail="Usuário inativo")

  if (datetime.now() > sessao["data_expiracao"]):
    raise HTTPException(status_code=401, detail="Sessão expirada")

  return sessao
