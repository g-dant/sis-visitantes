const MODO_MODAL = {
  NOVO: "NOVO",
  VISUALIZACAO: "VISUALIZACAO",
  EDICAO: "EDICAO"
};

let modoModal = MODO_MODAL.NOVO;

const botoes_visitante = ["btn-buscar-visitante", "btn-buscar-rg"];
const botoes_veiculo = ["btn-buscar-veiculo"];
const botoes_empresa = ["btn-adicionar-empresa"];
const botoes_salvar = ["btn-salvar-autorizacao"];
const controle_qr_code = ["qrcode-autorizacao"];

const campos_editaveis = [
  "visitante-cpf", 
  "visitante-rg", 
  "visitante-nome", 
  "visitante-email", 
  "visitante-celular", 
  "empresa-nome", 
  "veiculo-placa", 
  "veiculo-marca", 
  "veiculo-cor", 
  "veiculo-tipo", 
  "veiculo-observacoes", 
  "primeiro-dia", 
  "ultimo-dia"];

let idAutorizacaoEmEdicao = null;
let idStatusAutorizacao = null;
let idSetorSolicitante = null;
let idAutorizacaoVisualizada = null;

function exibirElementos(ids, exibir) {

  for (const id of ids) {

    const elemento = document.getElementById(id);
    if (!elemento) {
      continue;
    }

    elemento.style.display = exibir ? "inline-block": "none";
  }
}

function setModalBloqueado(bloqueado) {

  for (const id of campos_editaveis) {

    const campo = document.getElementById(id);
    if (!campo) { 
      continue;
    }

    campo.readOnly = bloqueado;
    campo.classList.toggle("campo-readonly", bloqueado);
  }
}

function configurarModoNovo() {

  setModalBloqueado(false);

  const cpf = document.getElementById("visitante-cpf");
  const rg = document.getElementById("visitante-rg");

  cpf.readOnly = false;
  rg.readOnly = false;

  cpf.classList.remove("campo-readonly");
  rg.classList.remove("campo-readonly");

  exibirElementos(botoes_visitante, true);
  exibirElementos(botoes_veiculo, true);
  exibirElementos(botoes_empresa, true);
  exibirElementos(botoes_salvar, true);

  exibirElementos(controle_qr_code, false);
}

function configurarModoVisualizacao() {

  setModalBloqueado(true);

  document.getElementById("visitante-cpf").readOnly = true;
  document.getElementById("visitante-rg").readOnly = true;

  exibirElementos(botoes_visitante, false);
  exibirElementos(botoes_veiculo, false);
  exibirElementos(botoes_empresa, false);
  exibirElementos(botoes_salvar, false);

  exibirElementos(controle_qr_code, true);
}

function configurarModoEdicao() {

  setModalBloqueado(false);

  const cpf = document.getElementById("visitante-cpf");
  const rg = document.getElementById("visitante-rg");

  cpf.readOnly = true;
  rg.readOnly = true;

  cpf.classList.add("campo-readonly");
  rg.classList.add("campo-readonly");

  exibirElementos(botoes_visitante, false);
  exibirElementos(botoes_veiculo, true);
  exibirElementos(botoes_empresa, false);
  exibirElementos(botoes_salvar, true);

  exibirElementos(controle_qr_code, false);
}


function openModalVisitantes() {

  document.getElementById("setor-solicitante").value =
    `${usuarioLogado.setor_codigo}: ${usuarioLogado.setor_descricao}`;

  document.getElementById("modalVisitantes").style.display = "flex";
}

function closeModalVisitantes() { 
  document.getElementById("modalVisitantes").style.display = "none"; 
}

function criarAutorizacao() {

  idAutorizacaoVisualizada = null;
  idAutorizacaoEmEdicao = null;
  limparModalAutorizacao();
  configurarModoNovo();
  openModalVisitantes();
}

async function setarCamposAutorizacao(autorizacao = {}) {

  idVisitante = autorizacao.id_visitante ?? null;
  idEmpresa = autorizacao.id_empresa ?? null;
  idVeiculo = autorizacao.id_veiculo ?? null;
  idStatusAutorizacao = autorizacao.id_status_autorizacao ?? null;
  idSetorSolicitante = autorizacao.id_setor_solicitante ?? null;

  document.getElementById("visitante-cpf").value = autorizacao.cpf || "";
  document.getElementById("visitante-rg").value = autorizacao.rg || "";
  document.getElementById("visitante-nome").value = autorizacao.visitante_nome || "";
  document.getElementById("visitante-email").value = autorizacao.email || "";
  document.getElementById("visitante-celular").value = autorizacao.celular || "";
  document.getElementById("empresa-nome").value = autorizacao.empresa_nome || "";
  document.getElementById("primeiro-dia").value = autorizacao.primeiro_dia;
  document.getElementById("ultimo-dia").value = autorizacao.ultimo_dia;
  document.getElementById("veiculo-placa").value = autorizacao.placa || "";
  document.getElementById("veiculo-marca").value = autorizacao.marca || "";
  document.getElementById("veiculo-cor").value = autorizacao.cor || "";
  document.getElementById("veiculo-tipo").value = autorizacao.tipo || "";

}

async function carregarAutorizacao(idAutorizacao) {

  const response = await fetch(`/autorizacoes/${idAutorizacao}`);
  if (!response.ok) {
    throw new Error("Erro ao buscar autorização");
  }

  return await response.json();
}

async function exibirAutorizacaoEmModoVisualizacao(autorizacao) {

  idAutorizacaoVisualizada = autorizacao.id;
  limparModalAutorizacao();

  await setarCamposAutorizacao(autorizacao);

  exibirStatusDestaque(autorizacao);
  configurarModoVisualizacao();
  openModalVisitantes();
}

async function visualizarAutorizacao(idAutorizacao) {
  
  idAutorizacaoVisualizada = idAutorizacao;
  const autorizacao = await carregarAutorizacao(idAutorizacao);
  await exibirAutorizacaoEmModoVisualizacao(autorizacao);  
}

async function editarAutorizacao(idAutorizacao) {

  idAutorizacaoVisualizada = null;
  idAutorizacaoEmEdicao = idAutorizacao;

  const autorizacao = await carregarAutorizacao(idAutorizacao);

  limparModalAutorizacao();
  setarCamposAutorizacao(autorizacao);
  ocultarStatusDestaque(autorizacao);
  configurarModoEdicao();
  openModalVisitantes();
}

function openUsersModal() { 
  document.getElementById("usersModal").style.display = "flex"; 
}

function closeModalUsuarios() { 
  document.getElementById("usersModal").style.display = "none"; 
}

function novoUsuario() {

  document.getElementById("userId").value = "";
  document.getElementById("userName").value = "";
  document.getElementById("userEmail").value = "";
  document.getElementById("userPhone").value = "";
  document.getElementById("userType").selectedIndex = 0;
}

function inicializarModalAutorizacao() {

  document
    .getElementById("empresa-nome")
    .addEventListener("input", pesquisarEmpresa);

  document
    .getElementById("visitante-cpf")
    .addEventListener("input", mascararCpf);

  document
    .getElementById("visitante-rg")
    .addEventListener("input", mascararRg);

  document
    .getElementById("veiculo-placa")
    .addEventListener("input", mascararPlaca);

  document
    .getElementById("visitante-celular")
    .addEventListener("input", mascararCelular);
}

function limparModalAutorizacao() {

  document.getElementById("status-autorizacao-destaque").style.display = "none";
  document.getElementById("status-visitante").style.display = "none";

  idVisitante = null;
  idVeiculo = null;
  idEmpresa = null;

  setarCamposAutorizacao();
  limparSugestoesEmpresa();
}

window.addEventListener(
  "click",
  function(event) {
    const modalVisitantes = document.getElementById("modalVisitantes");
    const usersModal = document.getElementById("usersModal");
    const modalImportacao = document.getElementById("modalImportacao");
    const modalRevisaoImportacao = document.getElementById("modalRevisaoImportacao");

    if (event.target === modalVisitantes) {
      closeModalVisitantes();
    }
    else if (event.target === usersModal) {
      closeModalUsuarios();
    }
    else if (event.target === modalImportacao) {
      fecharModalImportacao();
    }
    else if (event.target === modalRevisaoImportacao) {
      fecharModalRevisaoImportacao();
    }

  }
);

function abrirModalImportacao() {
  document.getElementById("modalImportacao").style.display = "flex";
}

function fecharModalImportacao() {
  document.getElementById("arquivo-importacao").value = "";
  document.getElementById("nome-arquivo-importacao").textContent = "Nenhum arquivo selecionado";
  document.getElementById("btn-importar-autorizacoes").disabled = true;
  document.getElementById("modalImportacao").style.display = "none";
}

function abrirModalRevisaoImportacao() {
    document.getElementById("modalRevisaoImportacao").style.display = "flex";
}

function fecharModalRevisaoImportacao() {
    document.getElementById("modalRevisaoImportacao").style.display = "none";
}
