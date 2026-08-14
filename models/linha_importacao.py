from dataclasses import dataclass, field

from models.autorizacao_importacao import AutorizacaoImportacao
from models.erro_importacao import ErroImportacao


@dataclass
class LinhaImportacao:

  # Número da linha na planilha original.
  # A contagem começa em 2, pois a primeira linha
  # contém o cabeçalho.
  numero: int

  # Dados da autorização extraídos da planilha.
  autorizacao: AutorizacaoImportacao

  # Indica se a linha pode ser importada.
  # Torna-se False quando há qualquer erro de validação.
  valida: bool = True

  # Lista de erros encontrados na linha.
  # Cada erro informa o campo afetado e a mensagem.
  erros: list[ErroImportacao] = field(default_factory=list)

  # Lista de avisos não bloqueantes.
  # Avisos não impedem a importação.
  avisos: list[str] = field(default_factory=list)

  # Indica se o usuário alterou manualmente
  # algum valor durante a pré-visualização.
  alterada: bool = False

  # Relação dos campos modificados pelo usuário.
  # Utilizada para destacar visualmente as correções.
  campos_alterados: list[str] = field(default_factory=list)

  # Indica que a linha colide com uma autorização
  # já existente no banco de dados.
  colisao_intervalo: bool = False

  # Indica que existem nomes diferentes associados
  # ao mesmo CPF dentro da própria planilha.
  nome_divergente: bool = False

  # Indica que existem empresas diferentes associadas
  # ao mesmo CPF dentro da própria planilha.
  empresa_divergente: bool = False

  # Nome cadastrado em banco de dados.
  nome_cadastrado: str | None = None

  # Nome na planilha
  nome_planilha: str | None = None

  # Indica se há nome no banco divergente daqueles
  # associados ao CPF
  nome_banco_divergente: bool = False

  @staticmethod
  def from_dict(dados: dict):
    return LinhaImportacao(
      
      numero=dados["numero"],

      autorizacao=AutorizacaoImportacao.from_dict(dados["autorizacao"]),
      
      valida=dados["valida"],
      
      erros=[ ErroImportacao.from_dict(erro) for erro in dados["erros"] ],
      
      avisos=dados["avisos"],
      
      alterada=dados["alterada"],
      
      campos_alterados=dados.get("campos_alterados", []),

      colisao_intervalo=dados.get("colisao_intervalo", False),
      
      nome_divergente = dados.get("nome_divergente", False),
      
      empresa_divergente = dados.get("empresa_divergente", False),

      nome_cadastrado=dados.get("nome_cadastrado"),

      nome_planilha=dados.get("nome_planilha"),
      
      nome_banco_divergente = dados.get("nome_banco_divergente", False))
