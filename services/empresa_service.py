from repositories.empresa_repository import EmpresaRepository


class EmpresaService:

  @staticmethod
  def listar():
    return EmpresaRepository.listar()


  @staticmethod
  def buscar_por_id(id_empresa: int):
    return EmpresaRepository.buscar_por_id(id_empresa)


  @staticmethod
  def criar(
    nome: str,
    cnpj: str,
    ativo: bool,
    conn=None):

    return EmpresaRepository.inserir(
      nome=nome,
      cnpj=cnpj,
      ativo=ativo,
      conn=conn)


  @staticmethod
  def atualizar_tudo(
    id_empresa: int,
    nome: str,
    cnpj: str,
    ativo: bool):

    return EmpresaRepository.atualizar_tudo(
      id_empresa=id_empresa,
      nome=nome,
      cnpj=cnpj,
      ativo=ativo)


  @staticmethod
  def excluir(id_empresa: int):
    return EmpresaRepository.excluir(id_empresa)


  @staticmethod
  def buscar_por_nome(nome: str):
    return EmpresaRepository.buscar_por_nome(nome)


  @staticmethod
  def buscar_por_nome_parcial(nome: str):
    return EmpresaRepository.buscar_por_nome_parcial(nome)
    

  @staticmethod
  def obter_ou_criar(nome, conn):

    empresa = EmpresaRepository.buscar_por_nome(nome, conn=conn)

    if empresa:
      return empresa["id"]

    return EmpresaRepository.inserir(
      nome=nome,
      cnpj="",
      ativo=True,
      conn=conn)
