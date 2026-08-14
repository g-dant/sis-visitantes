from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import (
  usuario_logado
)

from models.tipo_usuario_request import (
  TipoUsuarioRequest
)

from services.tipo_usuario_service import (
  TipoUsuarioService
)


router = APIRouter()


@router.get("/tipos")
def listar_tipos(
  sessao = Depends(usuario_logado)
):

  return TipoUsuarioService.listar()


@router.get("/tipos/{id_tipo}")
def buscar_tipo(
  id_tipo: int,
  sessao = Depends(usuario_logado)
):

  return TipoUsuarioService.buscar_por_id(
    id_tipo
  )


@router.post("/tipos")
def criar_tipo(
  request: TipoUsuarioRequest,
  sessao = Depends(usuario_logado)
):

  id_tipo = TipoUsuarioService.criar(
    nome=request.nome,
    ativo=request.ativo
  )

  return {
    "id": id_tipo
  }


@router.put("/tipos/{id_tipo}")
def atualizar_tipo(
  id_tipo: int,
  request: TipoUsuarioRequest,
  sessao = Depends(usuario_logado)
):

  TipoUsuarioService.atualizar_tudo(
    id_tipo=id_tipo,
    nome=request.nome,
    ativo=request.ativo
  )

  return {
    "mensagem": "Tipo atualizado com sucesso"
  }


@router.delete("/tipos/{id_tipo}")
def excluir_tipo(
  id_tipo: int,
  sessao = Depends(usuario_logado)
):

  TipoUsuarioService.excluir(
    id_tipo
  )

  return {
    "mensagem": "Tipo excluído com sucesso"
  }
