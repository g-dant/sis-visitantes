from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from models.status_autorizacao_request import (
  StatusAutorizacaoRequest
)

from services.status_autorizacao_service import (
  StatusAutorizacaoService
)


router = APIRouter()


@router.get("/status-autorizacoes")
def listar_status(
  sessao = Depends(usuario_logado)
):

  return StatusAutorizacaoService.listar()


@router.get("/status-autorizacoes/{id_status}")
def buscar_status(
  id_status: int,
  sessao = Depends(usuario_logado)
):

  return StatusAutorizacaoService.buscar_por_id(
    id_status
  )


@router.post("/status-autorizacoes")
def criar_status(
  request: StatusAutorizacaoRequest,
  sessao = Depends(usuario_logado)
):

  id_status = StatusAutorizacaoService.criar(
    nome=request.nome,
    descricao=request.descricao,
    ativo=request.ativo
  )

  return {
    "id": id_status
  }


@router.put("/status-autorizacoes/{id_status}")
def atualizar_status(
  id_status: int,
  request: StatusAutorizacaoRequest,
  sessao = Depends(usuario_logado)
):

  StatusAutorizacaoService.atualizar_tudo(
    id_status=id_status,
    nome=request.nome,
    descricao=request.descricao,
    ativo=request.ativo
  )

  return {
    "mensagem": "Status atualizado com sucesso"
  }


@router.delete("/status-autorizacoes/{id_status}")
def excluir_status(
  id_status: int,
  sessao = Depends(usuario_logado)
):

  StatusAutorizacaoService.excluir(
    id_status
  )

  return {
    "mensagem": "Status excluído com sucesso"
  }
