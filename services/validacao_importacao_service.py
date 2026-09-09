from models.autorizacao_importacao import AutorizacaoImportacao
from models.erro_importacao import ErroImportacao
from models.linha_importacao import LinhaImportacao
from models.resultado_importacao import ResultadoImportacao

from repositories.autorizacao_repository import AutorizacaoRepository
from repositories.visitante_repository import VisitanteRepository

from utils.cpf_utils import CpfUtils


class ValidacaoImportacaoService:

  # Trata-se do processo que valida linha por linha as planilhas de autorização importadas
  # Não inclui verificação de HEADERS da planilha importada
  # Tal validação se encontra como método estático em NormalizadorImportacaoService

  @staticmethod
  def validar(autorizacoes: list[AutorizacaoImportacao]) -> ResultadoImportacao:
  
    linhas = []
    erros_globais = []
  
    for indice, autorizacao in enumerate(autorizacoes, start=2):
  
      linha = LinhaImportacao(numero=indice, autorizacao=autorizacao)
      linha = ValidacaoImportacaoService.validar_linha(linha)
  
      if linha.valida:
      
        colisao = AutorizacaoRepository.buscar_colisao(
          autorizacao.cpf,
          autorizacao.primeiro_dia,
          autorizacao.ultimo_dia)
      
        if colisao is not None:
      
          linha.valida = False
          linha.colisao_intervalo = True
      
          if len(erros_globais) == 0:
      
            erros_globais.append(
              "Erro: há visitante(s) com autorizações "
              "que colidem com prazos já adicionados. "
              "Corrija a planilha e tente novamente.")
        
      linhas.append(linha)
 
    ValidacaoImportacaoService.__validar_coerencia_planilha(
      linhas)

    return ResultadoImportacao(
      sucesso=len(erros_globais) == 0,
      mensagem="",
      linhas=linhas,
      erros_globais=erros_globais)

  @staticmethod
  def __adicionar_erro(
    linha: LinhaImportacao, campo: str, mensagem: str) -> None:

    # Validar se já existe erro com mesma descrição
    erro_ja_existe = any(erro.mensagem == mensagem for erro in linha.erros)

    if erro_ja_existe:
      return

    linha.valida = False
    linha.erros.append(ErroImportacao(
      campo=campo, mensagem=mensagem))

  @staticmethod
  def __validar_cpf(linha: LinhaImportacao) -> None:

    autorizacao = linha.autorizacao
    cpf = CpfUtils.limpar(autorizacao.cpf)
    autorizacao.cpf = cpf

    if not cpf:
      ValidacaoImportacaoService.__adicionar_erro(
        linha, "cpf", "CPF não informado.")

      return

    if not CpfUtils.validar(cpf):
      ValidacaoImportacaoService.__adicionar_erro(
        linha, "cpf", "CPF inválido.")

  @staticmethod
  def __validar_nome(
    linha: LinhaImportacao) -> None:

    autorizacao = linha.autorizacao
    if autorizacao.nome:
      return

    ValidacaoImportacaoService.__adicionar_erro(
      linha, "nome", "Nome não informado.")

  @staticmethod
  def __validar_datas(linha: LinhaImportacao) -> None:

    autorizacao = linha.autorizacao

    if not autorizacao.primeiro_dia:
      ValidacaoImportacaoService.__adicionar_erro(
        linha, "primeiro_dia", "Primeiro dia não informado.")

    if not autorizacao.ultimo_dia:
      ValidacaoImportacaoService.__adicionar_erro(
        linha, "ultimo_dia", "Último dia não informado.")

  @staticmethod
  def validar_linha(linha: LinhaImportacao) -> LinhaImportacao:
    
    linha.valida = True
    
    linha.colisao_intervalo = False
    linha.nome_divergente = False
    linha.empresa_divergente = False
    
    linha.erros.clear()
    linha.avisos.clear()
    
    ValidacaoImportacaoService.__validar_cpf(linha)
    ValidacaoImportacaoService.__validar_nome(linha)
    ValidacaoImportacaoService.__validar_datas(linha)
    ValidacaoImportacaoService.__validar_placa(linha)
    ValidacaoImportacaoService.__validar_nome_banco(linha)
    
    return linha

  @staticmethod
  def __validar_placa(linha: LinhaImportacao):
    
    autorizacao = linha.autorizacao
    
    if autorizacao.placa is None:
      autorizacao.placa = ""
      return
   
    autorizacao.placa = autorizacao.placa.strip()

    if not autorizacao.placa:
      autorizacao.placa = ""
      return

  @staticmethod
  def __validar_coerencia_planilha(linhas: list[LinhaImportacao]):
  
    cpfs_nomes = {}
    cpfs_empresas = {}
  
    #
    # Primeira passagem:
    # constrói os mapas.
    #
  
    for linha in linhas:
  
      cpf = linha.autorizacao.cpf
  
      if not cpf:
        continue
  
      nome = (linha.autorizacao.nome or "").strip().upper()
      empresa = (linha.autorizacao.empresa or "").strip().upper()
  
      cpfs_nomes.setdefault(cpf, set()).add(nome)
      cpfs_empresas.setdefault(cpf, set()).add(empresa)
  
    #
    # Segunda passagem:
    # marca os erros.
    #
  
    for linha in linhas:
  
      cpf = linha.autorizacao.cpf
  
      if not cpf:
        continue
  
      nomes = cpfs_nomes.get(cpf, set())
      empresas = cpfs_empresas.get(cpf, set())
  
      if len(nomes) > 1:
  
        linha.valida = False
        linha.nome_divergente = True
  
        ValidacaoImportacaoService.__adicionar_erro(
          linha, "cpf", "Nomes diferentes para mesmo CPF.")

        ValidacaoImportacaoService.__adicionar_erro(
          linha, "nome", "Nomes diferentes para mesmo CPF.")
  
      if len(empresas) > 1:
  
        linha.valida = False
        linha.empresa_divergente = True
 
        ValidacaoImportacaoService.__adicionar_erro(
          linha, "cpf", "Empresas diferentes para mesmo CPF.")

        ValidacaoImportacaoService.__adicionar_erro(
          linha, "empresa", "Empresas diferentes para mesmo CPF.")

  @staticmethod
  def __validar_nome_banco(linha: LinhaImportacao):
  
    cpf = linha.autorizacao.cpf
  
    if not cpf:
      return

    if not linha.autorizacao.nome:
      return
  
    visitante = VisitanteRepository.buscar_por_cpf(cpf)
    if visitante is None:
      return
  
    nome_planilha = (linha.autorizacao.nome.strip().upper())
    nome_banco = (visitante["nome"].strip().upper())
  
    if nome_planilha == nome_banco:
      return
  
    linha.nome_banco_divergente = True
    linha.nome_planilha = linha.autorizacao.nome
    linha.nome_cadastrado = visitante["nome"]
    linha.avisos.append("Nome divergente.")
