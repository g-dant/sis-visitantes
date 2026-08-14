from fastapi import APIRouter
from fastapi import Depends

from security.auth_guard import usuario_logado

from models.visitante_veiculo_request import (
  VisitanteVeiculoRequest
)

from services.visitante_veiculo_service import (
  VisitanteVeiculoService
)


router = APIRouter()


@router.get("/visitante-veiculos")
def listar_relacoes(
  sessao = Depends(usuario_logado)
):

  return VisitanteVeiculoService.listar()


@router.get("/visitante-veiculos/{id_relacao}")
def buscar_relacao(
  id_relacao: int,
  sessao = Depends(usuario_logado)
):

  return VisitanteVeiculoService.buscar_por_id(
    id_relacao
  )


@router.post("/visitante-veiculos")
def criar_relacao(
  request: VisitanteVeiculoRequest,
  sessao = Depends(usuario_logado)
):

  id_relacao = VisitanteVeiculoService.criar(
    request.id_visitante,
    request.id_veiculo
  )

  return {
    "id": id_relacao
  }


@router.put("/visitante-veiculos/{id_relacao}")
def atualizar_relacao(
  id_relacao: int,
  request: VisitanteVeiculoRequest,
  sessao = Depends(usuario_logado)
):

  VisitanteVeiculoService.atualizar_tudo(
    id_relacao,
    request.id_visitante,
    request.id_veiculo
  )

  return {
    "mensagem": "Relação atualizada com sucesso"
  }


@router.delete("/visitante-veiculos/{id_relacao}")
def excluir_relacao(
  id_relacao: int,
  sessao = Depends(usuario_logado)
):

  VisitanteVeiculoService.excluir(
    id_relacao
  )

  return {
    "mensagem": "Relação excluída com sucesso"
  }


@router.get(
  "/visitantes/{id_visitante}/veiculos/placa/{placa}"
)
def buscar_veiculo_por_visitante_e_placa(
  id_visitante: int,
  placa: str,
  sessao=Depends(
    usuario_logado
  )
):

  return (
    VisitanteVeiculoService
    .buscar_veiculo_por_visitante_e_placa(
      id_visitante=id_visitante,
      placa=placa
    )
  )
