from fastapi import APIRouter
from fastapi import Depends

from security.permissoes import exigir_permissao

from models.visitante_request import VisitanteRequest
from services.visitante_service import VisitanteService


router = APIRouter()


@router.get("/visitantes")
def listar_visitantes(sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return VisitanteService.listar()

@router.get("/visitantes/cpf/{cpf}")
def buscar_visitante_por_cpf(cpf: str, sessao=Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):

  return VisitanteService.buscar_por_cpf(cpf)

@router.get("/visitantes/{id_visitante}")
def buscar_visitante(id_visitante: int, sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return VisitanteService.buscar_por_id(id_visitante)

@router.post("/visitantes")
def criar_visitante(request: VisitanteRequest, sessao = Depends(exigir_permissao("VISITANTE_CRIAR"))):

  id_visitante = VisitanteService.criar(
    request.nome,
    request.email,
    request.celular,
    request.rg,
    request.cpf,
    request.id_empresa,
    request.ativo)

  return { "id": id_visitante }

@router.put("/visitantes/{id_visitante}")
def atualizar_visitante(
  id_visitante: int, request: VisitanteRequest, sessao = Depends(exigir_permissao("VISITANTE_EDITAR"))):

  VisitanteService.atualizar_tudo(
    id_visitante,
    request.nome,
    request.email,
    request.celular,
    request.rg,
    request.cpf,
    request.id_empresa,
    request.ativo)

  return { "mensagem": "Visitante atualizado com sucesso" }


@router.delete("/visitantes/{id_visitante}")
def excluir_visitante(id_visitante: int, sessao = Depends(exigir_permissao("VISITANTE_EXCLUIR"))):

  VisitanteService.excluir(id_visitante)
  return { "mensagem": "Visitante excluído com sucesso" }
