from fastapi import APIRouter, Depends, HTTPException

from security.auth_guard import usuario_logado
from security.permissoes import exigir_permissao

from services.usuario_service import UsuarioService
from services.permissao_service import PermissaoService
from services.sessao_service import SessaoService

from models.usuario_atualizacao import UsuarioAtualizacao
from models.usuario_request import UsuarioRequest
from models.usuario_update_request import UsuarioUpdateRequest

router = APIRouter()


@router.get("/eu")
def eu(sessao = Depends(usuario_logado)):
  return SessaoService.obter_contexto(sessao)


@router.patch("/eu")
def atualizar_usuario_logado(
  dados: UsuarioAtualizacao,
  sessao = Depends(usuario_logado)):

  try:

    UsuarioService.atualizar_usuario_logado(
      id_usuario=sessao["id_usuario"],
      email=dados.email,
      senha=dados.senha)

    return { "mensagem": "Usuário atualizado."}

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))


@router.get("/usuarios")
def listar_usuarios(sessao = Depends(exigir_permissao("USUARIO_VISUALIZAR"))):
    return UsuarioService.listar()


@router.post("/usuarios")
def criar_usuario(
  request: UsuarioRequest,
  sessao = Depends(exigir_permissao("USUARIO_CRIAR"))):

  id_usuario = UsuarioService.criar(
    nome=request.nome,
    email=request.email,
    telefone=request.telefone,
    id_tipo=request.id_tipo,
    id_setor=request.id_setor,
    id_credencial=request.id_credencial,
    senha=request.senha)

  return { "id": id_usuario }


@router.get("/usuarios/{id_usuario}")
def buscar_usuario(id_usuario: int, sessao = Depends(exigir_permissao("USUARIO_VISUALIZAR"))):
    return UsuarioService.buscar_por_id(id_usuario)


@router.put("/usuarios/{id_usuario}")
def atualizar_usuario(

  id_usuario: int,
  request: UsuarioUpdateRequest,
  sessao = Depends(exigir_permissao("USUARIO_EDITAR"))):

  try:

    UsuarioService.atualizar_tudo(
      id_usuario=id_usuario,
      nome=request.nome,
      email=request.email,
      telefone=request.telefone,
      id_tipo=request.id_tipo,
      id_setor=request.id_setor,
      id_credencial=request.id_credencial,
      senha=request.senha,
      ativo=request.ativo)

    return { "mensagem": "Usuário atualizado com sucesso" }

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))


@router.delete("/usuarios/{id_usuario}")
def excluir_usuario( id_usuario: int, sessao = Depends(exigir_permissao("USUARIO_EXCLUIR"))):

  UsuarioService.excluir(id_usuario)
  return { "mensagem": "Usuário excluído com sucesso" }
