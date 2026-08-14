from fastapi import APIRouter, Depends
from security.auth_guard import usuario_logado
from services.painel_autorizacao_service import PainelAutorizacaoService
from services.parametro_sistema_service import ParametroSistemaService


router = APIRouter()

@router.get("/painel-autorizacao")
def buscar_painel(sessao = Depends(usuario_logado)):
  return PainelAutorizacaoService.buscar()

@router.get("/painel-autorizacao/configuracao")
def buscar_configuracao_painel(sessao = Depends(usuario_logado)):
  return { "refresh_ms": 
    ParametroSistemaService.obter("TEMPO_REFRESH_PAINEL_MS") }
