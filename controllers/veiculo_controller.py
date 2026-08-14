from fastapi import APIRouter
from fastapi import Depends
from security.auth_guard import usuario_logado
from models.veiculo_request import VeiculoRequest
from services.veiculo_service import VeiculoService


router = APIRouter()

@router.get("/veiculos")
def listar_veiculos(sessao = Depends(usuario_logado)):
  return VeiculoService.listar()

@router.get("/veiculos/placa/{placa}")
def buscar_por_placa(placa: str):
  return VeiculoService.buscar_por_placa(placa)

@router.get("/veiculos/{id_veiculo}")
def buscar_veiculo(id_veiculo: int, sessao = Depends(usuario_logado)):
  return VeiculoService.buscar_por_id(id_veiculo)


@router.post("/veiculos")
def criar_veiculo(
  request: VeiculoRequest,
  sessao = Depends(usuario_logado)
):

  id_veiculo = VeiculoService.criar(
    placa=request.placa,
    cor=request.cor,
    marca=request.marca,
    tipo=request.tipo,
    observacoes=request.observacoes,
    ativo=request.ativo
  )

  return {
    "id": id_veiculo
  }


@router.put("/veiculos/{id_veiculo}")
def atualizar_veiculo(
  id_veiculo: int,
  request: VeiculoRequest,
  sessao = Depends(usuario_logado)
):

  VeiculoService.atualizar_tudo(
    id_veiculo=id_veiculo,
    placa=request.placa,
    cor=request.cor,
    marca=request.marca,
    tipo=request.tipo,
    observacoes=request.observacoes,
    ativo=request.ativo
  )

  return {
    "mensagem": "Veículo atualizado com sucesso"
  }


@router.delete("/veiculos/{id_veiculo}")
def excluir_veiculo(
  id_veiculo: int,
  sessao = Depends(usuario_logado)
):

  VeiculoService.excluir(
    id_veiculo
  )

  return {
    "mensagem": "Veículo excluído com sucesso"
  }
