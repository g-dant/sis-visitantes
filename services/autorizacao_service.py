from dataclasses import asdict

from models.linha_importacao import LinhaImportacao
from models.resultado_importacao import ResultadoImportacao

from repositories.autorizacao_repository import AutorizacaoRepository
from repositories.status_autorizacao_repository import StatusAutorizacaoRepository
from repositories.visitante_repository import VisitanteRepository

from services.historico_autorizacao_service import HistoricoAutorizacaoService
from services.importacao_autorizacoes_service import ImportacaoAutorizacoesService
from services.importacao_persistencia_service import ImportacaoPersistenciaService
from services. validacao_importacao_service import ValidacaoImportacaoService


class AutorizacaoService:

  @staticmethod
  def listar():
    return AutorizacaoRepository.listar()


  @staticmethod
  def buscar_por_id(id_autorizacao: int):
    return AutorizacaoRepository.buscar_por_id(id_autorizacao)


  @staticmethod
  def criar(
    id_visitante: int,
    id_empresa: int,
    id_status_autorizacao: int,
    id_setor_solicitante: int,
    id_veiculo: int | None,
    primeiro_dia,
    ultimo_dia,
    id_usuario_logado: int,
    conn=None):
  
    id_autorizacao = AutorizacaoRepository.inserir(
      id_visitante=id_visitante,
      id_empresa=id_empresa,
      id_status_autorizacao=id_status_autorizacao,
      id_setor_solicitante=id_setor_solicitante,
      id_veiculo=id_veiculo,
      primeiro_dia=primeiro_dia,
      ultimo_dia=ultimo_dia,
      conn=conn)
  
    HistoricoAutorizacaoService.registrar_criacao(
      id_autorizacao=id_autorizacao,
      id_usuario=id_usuario_logado,
      conn=conn)
  
    return id_autorizacao


  @staticmethod
  def atualizar_tudo(
    id_autorizacao: int,
    id_visitante: int,
    id_empresa: int,
    id_status_autorizacao: int,
    id_setor_solicitante: int,
    id_veiculo: int | None,
    primeiro_dia,
    ultimo_dia,
    id_usuario_logado: int):
  
    autorizacao_atual = AutorizacaoRepository.buscar_por_id(id_autorizacao)
 
    status_novo = StatusAutorizacaoRepository.buscar_por_id(
      id_status_autorizacao)

    if status_novo["participa_colisao"]:

      visitante = VisitanteRepository.buscar_por_id(id_visitante)
      colisao = AutorizacaoRepository.buscar_colisao(
        cpf=visitante["cpf"],
        primeiro_dia=primeiro_dia,
        ultimo_dia=ultimo_dia,
        id_autorizacao_ignorada=id_autorizacao)

      if colisao is not None:

        raise ValueError(
          "Erro: uma autorização "
          "para esse mesmo visitante, "
          "no prazo de "
          f"{colisao['primeiro_dia'].strftime('%d/%m/%Y')} "
          "a "
          f"{colisao['ultimo_dia'].strftime('%d/%m/%Y')}, "
          "já foi emitida. "
          "Os intervalos de tempo "
          "não podem colidir.")

    AutorizacaoRepository.atualizar_tudo(
      id_autorizacao=id_autorizacao,
      id_visitante=id_visitante,
      id_empresa=id_empresa,
      id_status_autorizacao_anterior=autorizacao_atual["id_status_autorizacao_anterior"],
      id_status_autorizacao=id_status_autorizacao,
      id_setor_solicitante=id_setor_solicitante,
      id_veiculo=id_veiculo,
      primeiro_dia=primeiro_dia,
      ultimo_dia=ultimo_dia)
  
    if (autorizacao_atual["id_status_autorizacao"] != id_status_autorizacao):
  
      status_novo = (
        StatusAutorizacaoRepository
        .buscar_por_id(id_status_autorizacao))
  
      HistoricoAutorizacaoService.registrar_status_alterado(
        id_autorizacao=id_autorizacao,
        id_usuario=id_usuario_logado,
        status_anterior=autorizacao_atual["status_nome"],
        status_novo=status_novo["nome"])
  
    periodo_anterior = (
      f"{autorizacao_atual['primeiro_dia']} "
      f"até "
      f"{autorizacao_atual['ultimo_dia']}")
  
    periodo_novo = (
      f"{primeiro_dia} "
      f"até "
      f"{ultimo_dia}")
  
    if periodo_anterior != periodo_novo:
  
      HistoricoAutorizacaoService.registrar_periodo_alterado(
        id_autorizacao=id_autorizacao,
        id_usuario=id_usuario_logado,
        periodo_anterior=periodo_anterior,
        periodo_novo=periodo_novo)
  
  
  # MÉTODO NÃO DEVE SER USADO PELO SISTEMA: AUTORIZAÇÕES SÃO
  # REVOGADAS COM MUDANÇA DE STATUS. BD NÃO IMPLEMENTA
  # CASCODE NAS FKS POR DEFAULT
  @staticmethod
  def excluir(id_autorizacao: int, id_usuario_logado: int):

    HistoricoAutorizacaoService.registrar_exclusao(
      id_autorizacao=id_autorizacao,
      id_usuario=id_usuario_logado)

    AutorizacaoRepository.excluir(id_autorizacao)


  @staticmethod
  def atualizar_status(id_autorizacao: int, id_status_autorizacao: int, id_usuario_logado: int):
    
    autorizacao_atual = AutorizacaoRepository.buscar_por_id(id_autorizacao)
    # EVITA REGISTROS DO TIPO "STATUS ALTERADO DE REVOGADO PARA REVOGADO"
    if (autorizacao_atual["id_status_autorizacao"] == id_status_autorizacao):
      return

    status_novo = StatusAutorizacaoRepository.buscar_por_id(id_status_autorizacao)
    
    if status_novo["participa_colisao"]:
    
      colisao = AutorizacaoRepository.buscar_colisao(
        cpf=autorizacao_atual["cpf"],
        primeiro_dia=autorizacao_atual["primeiro_dia"],
        ultimo_dia=autorizacao_atual["ultimo_dia"],
        id_autorizacao_ignorada=id_autorizacao)
    
      if colisao is not None:
    
        raise ValueError(
          "Erro: uma autorização para "
          "esse mesmo visitante, no "
          f"prazo de "
          f"{colisao['primeiro_dia'].strftime('%d/%m/%Y')} "
          "a "
          f"{colisao['ultimo_dia'].strftime('%d/%m/%Y')}, "
          "já foi emitida. Os "
          "intervalos de tempo "
          "não podem colidir.")
    
    AutorizacaoRepository.atualizar_status(
      id_autorizacao=id_autorizacao,
      id_status_autorizacao_anterior=autorizacao_atual["id_status_autorizacao"],
      id_status_autorizacao=id_status_autorizacao)
    
    HistoricoAutorizacaoService.registrar_status_alterado(
      id_autorizacao=id_autorizacao,
      id_usuario=id_usuario_logado,
      status_anterior=autorizacao_atual["status_nome"],
      status_novo=status_novo["nome"])

  @staticmethod
  def listar_status_exibicao():
    return AutorizacaoRepository.listar_status_exibicao()

  @staticmethod
  def importar(arquivo):
  
      resultado = ImportacaoAutorizacoesService.importar(arquivo)
      return asdict(resultado)

  @staticmethod
  def revalidar_linha(dados: dict):
  
    linha = LinhaImportacao.from_dict(dados)
    linha = ValidacaoImportacaoService.validar_linha(linha)
    linha.colisao_intervalo = False
  
    if linha.valida:
  
      autorizacao = linha.autorizacao
  
      colisao = AutorizacaoRepository.buscar_colisao(
        autorizacao.cpf, autorizacao.primeiro_dia, autorizacao.ultimo_dia)
  
      if colisao is not None:
  
        linha.valida = False
        linha.colisao_intervalo = True
  
    return asdict(linha)

  @staticmethod
  def revalidar_planilha(dados: dict):
  
    resultado = ResultadoImportacao.from_dict(dados)
    autorizacoes = [ linha.autorizacao for linha in resultado.linhas]
    resultado = ValidacaoImportacaoService.validar(autorizacoes)
  
    return asdict(resultado)

  @staticmethod
  def confirmar_importacao(resultado: dict, sessao):

    resultado = ResultadoImportacao.from_dict(resultado)
    autorizacoes = [ linha.autorizacao for linha in resultado.linhas ]
    resultado_validacao = ValidacaoImportacaoService.validar(autorizacoes)

    for linha in resultado_validacao.linhas:
      if not linha.valida:
        raise ValueError(f"A linha {linha.numero} possui erros.")

    ImportacaoPersistenciaService.importar(resultado_validacao, sessao)

    return {
      "sucesso": True,
      "mensagem": "Importação realizada com sucesso." }

  @staticmethod
  def atualizar_periodo(
      id_autorizacao: int,
      primeiro_dia,
      ultimo_dia,
      id_usuario_logado: int):
  
    autorizacao_atual = AutorizacaoRepository.buscar_por_id(
      id_autorizacao)
  
    status_atual = StatusAutorizacaoRepository.buscar_por_id(
      autorizacao_atual["id_status_autorizacao"])
  
    if status_atual["participa_colisao"]:
  
      colisao = AutorizacaoRepository.buscar_colisao(
        cpf=autorizacao_atual["cpf"],
        primeiro_dia=primeiro_dia,
        ultimo_dia=ultimo_dia,
        id_autorizacao_ignorada=id_autorizacao)
  
      if colisao is not None:
  
        raise ValueError(
          "Erro: uma autorização para "
          "esse mesmo visitante, no "
          f"prazo de "
          f"{colisao['primeiro_dia'].strftime('%d/%m/%Y')} "
          "a "
          f"{colisao['ultimo_dia'].strftime('%d/%m/%Y')}, "
          "já foi emitida. Os "
          "intervalos de tempo "
          "não podem colidir.")
  
    periodo_anterior = (
      f"{autorizacao_atual['primeiro_dia']} "
      "até "
      f"{autorizacao_atual['ultimo_dia']}")
  
    periodo_novo = (
      f"{primeiro_dia} "
      "até "
      f"{ultimo_dia}")
  
    AutorizacaoRepository.atualizar_periodo(
      id_autorizacao=id_autorizacao,
      primeiro_dia=primeiro_dia,
      ultimo_dia=ultimo_dia)
  
    if periodo_anterior != periodo_novo:
  
      HistoricoAutorizacaoService.registrar_periodo_alterado(
        id_autorizacao=id_autorizacao,
        id_usuario=id_usuario_logado,
        periodo_anterior=periodo_anterior,
        periodo_novo=periodo_novo)
