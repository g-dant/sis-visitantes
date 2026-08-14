from config.database import get_connection

from services.empresa_service import EmpresaService
from services.historico_autorizacao_service import HistoricoAutorizacaoService
from services.parametro_sistema_service import ParametroSistemaService
from services.veiculo_service import VeiculoService
from services.visitante_service import VisitanteService

from repositories.autorizacao_repository import AutorizacaoRepository


class ImportacaoPersistenciaService:

  @staticmethod
  def importar(resultado_importacao, sessao):

    conn = get_connection()

    try:

      for linha in resultado_importacao.linhas:

        id_empresa = EmpresaService.obter_ou_criar(
          linha.autorizacao.empresa,
          conn)

        visitante = VisitanteService.obter_ou_criar(
          linha.autorizacao,
          id_empresa,
          conn)        
 
        veiculo = VeiculoService.obter_ou_criar(linha.autorizacao.placa, conn)

        id_autorizacao = AutorizacaoRepository.inserir(
          id_visitante=visitante,
          id_empresa=id_empresa,
          id_status_autorizacao=ParametroSistemaService.obter("STATUS_AUTORIZACAO_LOTE_PADRAO"),
          id_setor_solicitante=sessao["id_setor"],
          id_veiculo=veiculo,
          primeiro_dia=linha.autorizacao.primeiro_dia,
          ultimo_dia=linha.autorizacao.ultimo_dia,
          conn=conn)

        HistoricoAutorizacaoService.registrar_criacao_lote(id_autorizacao, sessao["id_usuario"], conn)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()
