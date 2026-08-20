from config.database import get_connection

from utils.normalizacao import somente_digitos

from repositories.empresa_repository import EmpresaRepository
from repositories.visitante_repository import VisitanteRepository


class VisitanteService:

  @staticmethod
  def listar():
    return VisitanteRepository.listar()


  @staticmethod
  def buscar_por_id(id_visitante):
    return VisitanteRepository.buscar_por_id(id_visitante)


  @staticmethod
  def criar(
    nome,
    email,
    celular,
    rg,
    cpf,
    id_empresa,
    ativo,
    conn=None):

    return VisitanteRepository.inserir(
      nome,
      email,
      celular,
      rg,
      cpf,
      id_empresa,
      ativo,
      conn)


  @staticmethod
  def atualizar_tudo(
    id_visitante,
    nome,
    email,
    celular,
    rg,
    cpf,
    id_empresa,
    ativo):

    return VisitanteRepository.atualizar_tudo(
      id_visitante,
      nome,
      email,
      celular,
      rg,
      cpf,
      id_empresa,
      ativo)


  @staticmethod
  def excluir(id_visitante: int):

    conn = get_connection()

    try:

      if VisitanteRepository.existe_autorizacao(
        id_visitante, conn=conn):
        raise ValueError(
          "O visitante não pode ser excluído porque "
          "está associado a uma ou mais autorizações.")

      VisitanteRepository.excluir_associacoes_veiculo(
        id_visitante, conn=conn)

      VisitanteRepository.excluir(
        id_visitante, conn=conn)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()


  @staticmethod
  def buscar_por_cpf(cpf: str):

    cpf = somente_digitos(cpf)
    return VisitanteRepository.buscar_por_cpf(cpf)

  @staticmethod
  def obter_ou_criar(autorizacao, id_empresa, conn):
  
    visitante = VisitanteRepository.buscar_por_cpf(
      autorizacao.cpf, conn=conn)

    if visitante:

      VisitanteRepository.atualizar_empresa(
        visitante["id"],
        id_empresa,
        conn)

      return visitante["id"]

    return VisitanteRepository.inserir(
      nome=autorizacao.nome,
      email=autorizacao.email,
      celular=autorizacao.celular,
      rg=autorizacao.rg,
      cpf=autorizacao.cpf,
      id_empresa=id_empresa,
      ativo=True,
      conn=conn)
