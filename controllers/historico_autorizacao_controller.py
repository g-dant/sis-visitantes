from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from services.historico_autorizacao_service import (
  HistoricoAutorizacaoService
)


router = APIRouter()


@router.get(
  "/autorizacoes/{id_autorizacao}/historico"
)
def listar_historico(
  id_autorizacao: int,
  sessao = Depends(usuario_logado)
):

  return (
    HistoricoAutorizacaoService
    .listar_por_autorizacao(
      id_autorizacao
    )
  )
