from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from security.auth_guard import usuario_logado
from security.permissoes import exigir_permissao

from models.alterar_status_request import AlterarStatusRequest
from models.autorizacao_request import AutorizacaoRequest
from models.linha_importacao import LinhaImportacao
from models.resultado_importacao import ResultadoImportacao

from services.autorizacao_service import AutorizacaoService


router = APIRouter()


@router.get("/autorizacoes")
def listar_autorizacoes(sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return AutorizacaoService.listar()


@router.get("/autorizacoes/importacao/modelo")
def baixar_modelo_importacao():
  return FileResponse(
    path="static/ods/modelo-importacao.ods",
    filename="modelo-importacao.ods",
    media_type="application/vnd.oasis.opendocument.spreadsheet")


@router.get("/autorizacoes/{id_autorizacao}")
def buscar_autorizacao(id_autorizacao: int, sessao = Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return AutorizacaoService.buscar_por_id(id_autorizacao)


@router.post("/autorizacoes")
def criar_autorizacao(request: AutorizacaoRequest, sessao = Depends(exigir_permissao("AUTORIZACAO_CRIAR"))):

  id_autorizacao = AutorizacaoService.criar(
    id_visitante=request.id_visitante,
    id_empresa=request.id_empresa,
    id_status_autorizacao=request.id_status_autorizacao,
    id_setor_solicitante=request.id_setor_solicitante,
    id_veiculo=request.id_veiculo,
    primeiro_dia=request.primeiro_dia,
    ultimo_dia=request.ultimo_dia,
    id_usuario_logado=sessao["id_usuario"])

  return { "id": id_autorizacao }


@router.put("/autorizacoes/{id_autorizacao}")
def atualizar_autorizacao(
  id_autorizacao: int,
  request: AutorizacaoRequest,
  sessao = Depends(exigir_permissao("AUTORIZACAO_EDITAR"))):
  
  try:
  
    AutorizacaoService.atualizar_periodo(
      id_autorizacao=id_autorizacao,
      primeiro_dia=request.primeiro_dia,
      ultimo_dia=request.ultimo_dia,
      id_usuario_logado=sessao["id_usuario"])
  
    return { "mensagem": "Autorização atualizada com sucesso" }
  
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  

@router.patch("/autorizacoes/{id_autorizacao}/status")
def alterar_status_autorizacao(
  id_autorizacao: int,
  request: AlterarStatusRequest,
  sessao = Depends(exigir_permissao("AUTORIZACAO_ALTERAR_STATUS"))):

  try:

    AutorizacaoService.atualizar_status(
      id_autorizacao=id_autorizacao,
      id_status_autorizacao=request.id_status_autorizacao,
      id_usuario_logado=sessao["id_usuario"])

    return { "mensagem": "Status atualizado com sucesso" }

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))


@router.delete("/autorizacoes/{id_autorizacao}")
def excluir_autorizacao(id_autorizacao: int, sessao = Depends(exigir_permissao("AUTORIZACAO_EXCLUIR"))):
  AutorizacaoService.excluir(id_autorizacao=id_autorizacao, id_usuario_logado=sessao["id_usuario"])
  return { "mensagem": "Autorização excluída com sucesso" }


@router.get("/autorizacoes-consulta/status-exibicao")
def listar_status_exibicao(sessao=Depends(exigir_permissao("AUTORIZACAO_VISUALIZAR"))):
  return AutorizacaoService.listar_status_exibicao()


@router.post("/autorizacoes/importar")
async def importar_autorizacoes(arquivo: UploadFile = File(...), sessao=Depends(exigir_permissao("AUTORIZACAO_IMPORTAR"))):
  return AutorizacaoService.importar(arquivo)


@router.post("/importacao/revalidar-linha")
def revalidar_linha(linha: dict):
  return AutorizacaoService.revalidar_linha(linha)


@router.post("/importacao/revalidar-planilha")
def revalidar_planilha(resultado: dict):
  return AutorizacaoService.revalidar_planilha(resultado)


@router.post("/importacao/confirmar")
def confirmar_importacao(resultado: dict, sessao = Depends(exigir_permissao("AUTORIZACAO_IMPORTAR"))):
  return AutorizacaoService.confirmar_importacao(resultado, sessao)


