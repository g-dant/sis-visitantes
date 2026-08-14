# TODO:
# executar fluxo completo em transação única
from config.database import get_connection

from repositories.autorizacao_repository import AutorizacaoRepository

from services.empresa_service import EmpresaService
from services.visitante_service import VisitanteService
from services.veiculo_service import VeiculoService
from services.autorizacao_service import AutorizacaoService
from services.parametro_sistema_service import ParametroSistemaService
from services.visitante_veiculo_service import VisitanteVeiculoService

from utils.normalizacao import normalizar_dto_emissao_autorizacao


class EmissaoAutorizacaoService:

  @staticmethod
  def emitir(dto, sessao):

    dto_normalizado = normalizar_dto_emissao_autorizacao(dto)
    conn = get_connection()

    try:
  
      empresa = (EmpresaService.buscar_por_nome(dto_normalizado.empresa_nome))
  
      if empresa is None:
        id_empresa = EmpresaService.criar(
          nome=dto_normalizado.empresa_nome, 
          cnpj=dto_normalizado.empresa_cnpj, 
          ativo=True,
          conn=conn)
  
      else:
        id_empresa = (empresa["id"])
  
      visitante = (VisitanteService.buscar_por_cpf(dto_normalizado.cpf))
  
      if visitante is None:
  
        id_visitante = VisitanteService.criar(
          nome=dto_normalizado.nome, 
          email=dto_normalizado.email,
          celular=dto_normalizado.celular,
          rg=dto_normalizado.rg,
          cpf=dto_normalizado.cpf,
          id_empresa=id_empresa,
          ativo=True,
          conn=conn)
  
      else:
        id_visitante = (visitante["id"])
  
      id_veiculo = None
  
      if dto_normalizado.placa:
  
        veiculo = (VeiculoService.buscar_por_placa(dto_normalizado.placa))
  
        if veiculo is None:
  
          id_veiculo = VeiculoService.criar(
            placa=dto_normalizado.placa,
            cor=dto_normalizado.cor,
            marca=dto_normalizado.marca,
            tipo=dto_normalizado.tipo,
            observacoes=(dto_normalizado.observacoes_veiculo),
            ativo=True,
            conn=conn)
  
        else:
          id_veiculo = (veiculo["id"])
  
        relacao = (VisitanteVeiculoService
          .buscar_por_visitante_e_veiculo(
          id_visitante=id_visitante,
          id_veiculo=id_veiculo))
  
        if relacao is None:
  
          VisitanteVeiculoService.criar(
            id_visitante=id_visitante,
            id_veiculo=id_veiculo,
            conn=conn)
  
      id_status_autorizacao = (ParametroSistemaService
        .obter_int("STATUS_AUTORIZACAO_PADRAO"))

      colisao = AutorizacaoRepository.buscar_colisao(
        dto_normalizado.cpf,
        dto_normalizado.primeiro_dia,
        dto_normalizado.ultimo_dia)

      if colisao is not None:
        
        inicio = colisao["primeiro_dia"].strftime("%d/%m/%Y")
        fim = colisao["ultimo_dia"].strftime("%d/%m/%Y")

        raise ValueError(
          "Erro: uma autorização para esse mesmo visitante, "
          f"no prazo de {inicio} a {fim}, já foi emitida. "
          "Os intervalos de tempo não podem colidir.")

      id_autorizacao = AutorizacaoService.criar(
          id_visitante=id_visitante,
          id_empresa=id_empresa,
          id_status_autorizacao=(id_status_autorizacao),
          id_setor_solicitante=(sessao["id_setor"]),
          id_veiculo=id_veiculo,
          primeiro_dia=dto_normalizado.primeiro_dia,
          ultimo_dia=dto_normalizado.ultimo_dia,
          id_usuario_logado=(sessao["id_usuario"]),
          conn=conn)

      conn.commit()
      return id_autorizacao

    except:
      conn.rollback()
      raise

    finally:
      conn.close()
