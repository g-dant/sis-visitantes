from fastapi import APIRouter, Depends, HTTPException

from models.emissao_autorizacao_dto import EmissaoAutorizacaoDTO
from security.auth_guard import usuario_logado
from services.emissao_autorizacao_service import EmissaoAutorizacaoService


router = APIRouter(tags=["Emissão de Autorização"])


@router.post("/autorizacoes/emissao")
def emitir_autorizacao(dto: EmissaoAutorizacaoDTO, 
  sessao=Depends(usuario_logado)):

  try:

    id_autorizacao = EmissaoAutorizacaoService.emitir(
      dto=dto, sessao=sessao)

    return { "id": id_autorizacao }

  except ValueError as e:

    raise HTTPException(
      status_code=400,
      detail=str(e))
