from fastapi import APIRouter, Depends

from security.auth_guard import usuario_logado
from services.token_qrcode_service import TokenQRCodeService
from services.autorizacao_service import AutorizacaoService


router = APIRouter()

@router.get("/autorizacoes/{id_autorizacao}/qrcode")
def gerar_qrcode(id_autorizacao: int, sessao=Depends(usuario_logado)):
  token = TokenQRCodeService.gerar_token(id_autorizacao)
  return { "url": f"/verificar/{token}" }

@router.get("/verificar/{token}")
def verificar_qrcode(token: str, sessao=Depends(usuario_logado)):
  id_autorizacao = (TokenQRCodeService.obter_id_autorizacao(token))
  return AutorizacaoService.buscar_por_id(id_autorizacao)
