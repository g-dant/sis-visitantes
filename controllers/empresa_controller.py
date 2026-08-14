from fastapi import ( APIRouter, Depends, Query )

from security.auth_guard import usuario_logado
from models.empresa_request import EmpresaRequest
from services.empresa_service import EmpresaService


router = APIRouter()


@router.get("/empresas")
def listar_empresas(
  sessao = Depends(usuario_logado)
):

  return EmpresaService.listar()


@router.get("/empresas/{id_empresa}")
def buscar_empresa(
  id_empresa: int,
  sessao = Depends(usuario_logado)
):

  return EmpresaService.buscar_por_id(
    id_empresa
  )


@router.post("/empresas")
def criar_empresa(
  request: EmpresaRequest,
  sessao = Depends(usuario_logado)
):

  id_empresa = EmpresaService.criar(
    nome=request.nome,
    cnpj=request.cnpj,
    ativo=request.ativo
  )

  return {
    "id": id_empresa
  }


@router.put("/empresas/{id_empresa}")
def atualizar_empresa(
  id_empresa: int,
  request: EmpresaRequest,
  sessao = Depends(usuario_logado)
):

  EmpresaService.atualizar_tudo(
    id_empresa=id_empresa,
    nome=request.nome,
    cnpj=request.cnpj,
    ativo=request.ativo
  )

  return {
    "mensagem": "Empresa atualizada com sucesso"
  }


@router.delete("/empresas/{id_empresa}")
def excluir_empresa(
  id_empresa: int,
  sessao = Depends(usuario_logado)
):

  EmpresaService.excluir(
    id_empresa
  )

  return {
    "mensagem": "Empresa excluída com sucesso"
  }


@router.get(
  "/empresas"
)
def buscar_por_nome_parcial(
  nome: str = Query(...)
):

  return (
    EmpresaService
    .buscar_por_nome_parcial(
      nome
    )
  )
