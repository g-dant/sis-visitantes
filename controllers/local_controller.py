from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from models.local_request import (
  LocalRequest
)

from services.local_service import (
  LocalService
)


router = APIRouter()


@router.get("/locais")
def listar_locais(
  sessao = Depends(usuario_logado)
):

  return LocalService.listar()


@router.get("/locais/{id_local}")
def buscar_local(
  id_local: int,
  sessao = Depends(usuario_logado)
):

  return LocalService.buscar_por_id(
    id_local
  )


@router.post("/locais")
def criar_local(
  request: LocalRequest,
  sessao = Depends(usuario_logado)
):

  id_local = LocalService.criar(
    codigo=request.codigo,
    descricao=request.descricao,
    ativo=request.ativo
  )

  return {
    "id": id_local
  }


@router.put("/locais/{id_local}")
def atualizar_local(
  id_local: int,
  request: LocalRequest,
  sessao = Depends(usuario_logado)
):

  LocalService.atualizar_tudo(
    id_local=id_local,
    codigo=request.codigo,
    descricao=request.descricao,
    ativo=request.ativo
  )

  return {
    "mensagem": "Local atualizado com sucesso"
  }


@router.delete("/locais/{id_local}")
def excluir_local(
  id_local: int,
  sessao = Depends(usuario_logado)
):

  LocalService.excluir(
    id_local
  )

  return {
    "mensagem": "Local excluído com sucesso"
  }
