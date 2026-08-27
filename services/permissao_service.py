from repositories.credencial_permissao_repository import CredencialPermissaoRepository


class PermissaoService:

  @staticmethod
  def credencial_possui_permissao(
      id_credencial: int,
      codigo_permissao: str):
  
      return CredencialPermissaoRepository.possui_permissao(
          id_credencial=id_credencial,
          codigo_permissao=codigo_permissao)

  @staticmethod
  def listar_permissoes(id_credencial: int):

    return CredencialPermissaoRepository.listar_permissoes(
      id_credencial=id_credencial)
      
  @staticmethod
  def listar_todas():
  
    return CredencialPermissaoRepository.listar_todas_permissoes()
    
  @staticmethod
  def listar_com_status(id_credencial: int):
  
    return CredencialPermissaoRepository.listar_permissoes_com_status(
      id_credencial=id_credencial)
