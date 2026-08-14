from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from models.credencial_request import (
  CredencialRequest
)

from services.credencial_service import (
  CredencialService
)


router = APIRouter()


@router.get("/credenciais")
def listar_credenciais(
  sessao = Depends(usuario_logado)
):

  return CredencialService.listar()


@router.get("/credenciais/{id_credencial}")
def buscar_credencial(
  id_credencial: int,
  sessao = Depends(usuario_logado)
):

  return CredencialService.buscar_por_id(
    id_credencial
  )


@router.post("/credenciais")
def criar_credencial(
  request: CredencialRequest,
  sessao = Depends(usuario_logado)
):

  id_credencial = CredencialService.criar(
    nome=request.nome,
    ativo=request.ativo
  )

  return {
    "id": id_credencial
  }


@router.put("/credenciais/{id_credencial}")
def atualizar_credencial(
  id_credencial: int,
  request: CredencialRequest,
  sessao = Depends(usuario_logado)
):

  CredencialService.atualizar_tudo(
    id_credencial=id_credencial,
    nome=request.nome,
    ativo=request.ativo
  )

  return {
    "mensagem": "Credencial atualizada com sucesso"
  }


@router.delete("/credenciais/{id_credencial}")
def excluir_credencial(
  id_credencial: int,
  sessao = Depends(usuario_logado)
):

  CredencialService.excluir(
    id_credencial
  )

  return {
    "mensagem": "Credencial excluída com sucesso"
  }
