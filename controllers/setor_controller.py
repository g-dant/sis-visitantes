from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from models.setor_request import (
  SetorRequest
)

from services.setor_service import (
  SetorService
)


router = APIRouter()


@router.get("/setores")
def listar_setores(
  sessao = Depends(usuario_logado)
):

  return SetorService.listar()


@router.get("/setores/{id_setor}")
def buscar_setor(
  id_setor: int,
  sessao = Depends(usuario_logado)
):

  return SetorService.buscar_por_id(
    id_setor
  )


@router.post("/setores")
def criar_setor(
  request: SetorRequest,
  sessao = Depends(usuario_logado)
):

  id_setor = SetorService.criar(
    codigo=request.codigo,
    descricao=request.descricao,
    ativo=request.ativo,
    id_local=request.id_local
  )

  return {
    "id": id_setor
  }


@router.put("/setores/{id_setor}")
def atualizar_setor(
  id_setor: int,
  request: SetorRequest,
  sessao = Depends(usuario_logado)
):

  SetorService.atualizar_tudo(
    id_setor=id_setor,
    codigo=request.codigo,
    descricao=request.descricao,
    ativo=request.ativo,
    id_local=request.id_local
  )

  return {
    "mensagem": "Setor atualizado com sucesso"
  }


@router.delete("/setores/{id_setor}")
def excluir_setor(
  id_setor: int,
  sessao = Depends(usuario_logado)
):

  SetorService.excluir(
    id_setor
  )

  return {
    "mensagem": "Setor excluído com sucesso"
  }
