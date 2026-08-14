from repositories.painel_autorizacao_repository import PainelAutorizacaoRepository


class PainelAutorizacaoService:

  @staticmethod
  def buscar():
    return PainelAutorizacaoRepository.buscar()
