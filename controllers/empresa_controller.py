from fastapi import ( APIRouter, Depends, Query )

from models.empresa_request import EmpresaRequest

from security.permissoes import exigir_permissao

from services.empresa_service import EmpresaService


router = APIRouter()

@router.get("/empresas")
def listar_empresas(sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return EmpresaService.listar()

@router.get("/empresas/busca")
def buscar_por_nome_parcial(
  nome: str = Query(...),
  sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return EmpresaService.buscar_por_nome_parcial(nome)

@router.get("/empresas/{id_empresa}")
def buscar_empresa(id_empresa: int, sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return EmpresaService.buscar_por_id(id_empresa)

@router.put("/empresas/{id_empresa}")
def atualizar_empresa(
  id_empresa: int,
  request: EmpresaRequest,
  sessao = Depends(exigir_permissao("EMPRESA_EDITAR"))):

  EmpresaService.atualizar_tudo(
    id_empresa=id_empresa,
    nome=request.nome,
    cnpj=request.cnpj,
    ativo=request.ativo)

  return { "mensagem": "Empresa atualizada com sucesso" }

@router.post("/empresas")
def criar_empresa(request: EmpresaRequest, sessao = Depends(exigir_permissao("EMPRESA_CRIAR"))):

  id_empresa = EmpresaService.criar(
    nome=request.nome,
    cnpj=request.cnpj,
    ativo=request.ativo)

  return { "id": id_empresa }
