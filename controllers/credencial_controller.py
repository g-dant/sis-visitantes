from fastapi import APIRouter
from fastapi import Depends

from models.credencial_request import CredencialRequest

from security.auth_guard import usuario_logado

from services.credencial_service import CredencialService
from services.permissao_service import PermissaoService


router = APIRouter()

@router.get("/credenciais")
def listar_credenciais(sessao = Depends(usuario_logado)):

  return CredencialService.listar()

@router.get("/credenciais/{id_credencial}")
def buscar_credencial(id_credencial: int, sessao = Depends(usuario_logado)):

  return CredencialService.buscar_por_id(id_credencial)
  
@router.get("/credenciais/{id_credencial}/permissoes")
def listar_permissoes_credencial(id_credencial: int, sessao = Depends(usuario_logado)):

  return PermissaoService.listar_com_status(id_credencial=id_credencial)

@router.post("/credenciais")
def criar_credencial(request: CredencialRequest, sessao = Depends(usuario_logado)):

  id_credencial = CredencialService.criar(
    nome=request.nome,
    descricao=request.descricao,
    ativo=request.ativo,
    ids_permissoes=request.ids_permissoes)

  return { "id": id_credencial }

@router.put("/credenciais/{id_credencial}")
def atualizar_credencial(
  id_credencial: int, 
  request: CredencialRequest,
  sessao = Depends(usuario_logado)):

  CredencialService.atualizar_tudo(
    id_credencial=id_credencial,
    nome=request.nome,
    descricao=request.descricao,
    ativo=request.ativo)

  return { "mensagem": "Credencial atualizada com sucesso" }

@router.delete("/credenciais/{id_credencial}")
def excluir_credencial(id_credencial: int,
  sessao = Depends(usuario_logado)):

  CredencialService.excluir(id_credencial)

  return { "mensagem": "Credencial excluída com sucesso" }
  
@router.get("/permissoes")
def listar_permissoes(sessao = Depends(usuario_logado)):
  return PermissaoService.listar_todas()

@router.post("/credenciais/{id_credencial}/permissoes/{id_permissao}")
def habilitar_permissao_credencial(
  id_credencial: int,
  id_permissao: int,
  sessao = Depends(usuario_logado)):

  CredencialService.habilitar_permissao(
    id_credencial=id_credencial,
    id_permissao=id_permissao)

  return { "mensagem": "Permissão habilitada com sucesso" }

@router.delete("/credenciais/{id_credencial}/permissoes/{id_permissao}")
def desabilitar_permissao_credencial(
  id_credencial: int,
  id_permissao: int,
  sessao = Depends(usuario_logado)):

  CredencialService.desabilitar_permissao(
    id_credencial=id_credencial,
    id_permissao=id_permissao)

  return { "mensagem": "Permissão desabilitada com sucesso" }
