from repositories.historico_autorizacao_repository import HistoricoAutorizacaoRepository

from config.historico_mensagens import (
  AUTORIZACAO_CRIADA,
  AUTORIZACAO_CRIADA_LOTE,
  AUTORIZACAO_EXCLUIDA,
  STATUS_ALTERADO,
  PERIODO_ALTERADO)


class HistoricoAutorizacaoService:

  @staticmethod
  def listar_por_autorizacao(id_autorizacao: int):
    return HistoricoAutorizacaoRepository.listar_por_autorizacao(id_autorizacao)


  @staticmethod
  def registrar(
    id_autorizacao: int,
    id_usuario: int,
    descricao: str,
    conn=None):

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      descricao,
      conn)


  @staticmethod
  def registrar_criacao(
    id_autorizacao: int,
    id_usuario: int,
    conn=None):

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      AUTORIZACAO_CRIADA,
      conn)


  @staticmethod
  def registrar_criacao_lote(
    id_autorizacao: int,
    id_usuario: int,
    conn=None):

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      AUTORIZACAO_CRIADA_LOTE,
      conn)


  @staticmethod
  def registrar_exclusao(
    id_autorizacao: int,
    id_usuario: int,
    conn=None):

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      AUTORIZACAO_EXCLUIDA,
      conn)


  @staticmethod
  def registrar_status_alterado(
    id_autorizacao: int,
    id_usuario: int,
    status_anterior: str,
    status_novo: str,
    conn=None):

    descricao = STATUS_ALTERADO.format(
      anterior=status_anterior,
      novo=status_novo)

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      descricao,
      conn)


  @staticmethod
  def registrar_periodo_alterado(
    id_autorizacao: int,
    id_usuario: int,
    periodo_anterior: str,
    periodo_novo: str,
    conn=None):

    descricao = PERIODO_ALTERADO.format(
      anterior=periodo_anterior,
      novo=periodo_novo)

    return HistoricoAutorizacaoRepository.inserir(
      id_autorizacao,
      id_usuario,
      descricao,
      conn)
