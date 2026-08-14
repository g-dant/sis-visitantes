from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import usuario_logado
from services.parametro_sistema_service import ParametroSistemaService
from security.permissoes import exigir_permissao

from models.parametro_sistema_request import ParametroSistemaRequest


router = APIRouter(tags=["Parâmetro Sistema"])


@router.get("/parametros_sistema")
def listar_parametros_sistema(sessao=Depends(exigir_permissao("PARAMETRO_SISTEMA_VISUALIZAR"))):
  return ParametroSistemaService.listar()


@router.get("/parametros_sistema/{id_parametro_sistema}")
def buscar_parametro_sistema(
  id_parametro_sistema: int,
  sessao=Depends(exigir_permissao("PARAMETRO_SISTEMA_VISUALIZAR"))):

  return ParametroSistemaService.buscar_por_id(id_parametro_sistema)


@router.post("/parametros_sistema")
def criar_parametro_sistema(
  request: ParametroSistemaRequest,
  sessao=Depends(exigir_permissao("PARAMETRO_SISTEMA_CRIAR"))):

  id_parametro_sistema = (
    ParametroSistemaService
    .criar(
      chave=request.chave,
      valor=request.valor
    )
  )

  return {
    "id": id_parametro_sistema
  }


@router.put("/parametros_sistema/{id_parametro_sistema}")
def atualizar_parametro_sistema(
  id_parametro_sistema: int,
  request: ParametroSistemaRequest,
  sessao=Depends(exigir_permissao("PARAMETRO_SISTEMA_EDITAR"))):

  ParametroSistemaService.atualizar_tudo(
    id_parametro_sistema=id_parametro_sistema,
    chave=request.chave,
    valor=request.valor)

  return {
    "mensagem":
    "Parâmetro atualizado com sucesso"
  }


@router.delete("/parametros_sistema/{id_parametro_sistema}")
def excluir_parametro_sistema(
  id_parametro_sistema: int,
  sessao=Depends(exigir_permissao("PARAMETRO_SISTEMA_EXCLUIR"))):

  ParametroSistemaService.excluir(id_parametro_sistema)

  return {
    "mensagem":
    "Parâmetro excluído com sucesso"
  }
