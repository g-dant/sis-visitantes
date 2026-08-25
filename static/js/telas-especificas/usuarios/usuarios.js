let usuarios = [];
let paginacaoUsuarios;

const filtroUsuarios = criarFiltroTabela({

  obterDados: () => usuarios,
  campoTextoId: "filtro-usuarios",
  camposTexto: [ "nome", "email", "telefone", "tipo_nome", "setor_descricao", "credencial_nome" ],

  filtros: [{
    elementoId: "filtro-ativo",
    aplicar: (usuario, valor) => (valor === "") || (String(usuario.ativo) === valor)
  }],

  aoFiltrar: () => { paginacaoUsuarios.reiniciar(); }
});

const estadoModalUsuario = {
  modo: "novo",
  idUsuario: null
};

document.getElementById("usuario-alterar-senha").addEventListener("change", atualizarEstadoAlteracaoSenha);

function criarLinhaUsuario(usuario) {

  const tr = document.createElement("tr");

  let botaoEditar = 
     `<button 
        class="btn btn-primary" 
	title="Editar usuário" 
	onclick="abrirEditarUsuario(${usuario.id})">
        <i class="fa-solid fa-pen"></i>
      </button>`;

  tr.innerHTML = `

    <td>${usuario.nome}</td>
    <td>${usuario.email}</td>
    <td>${usuario.telefone ?? ""}</td>
    <td>${usuario.tipo_nome}</td>
    <td>${usuario.setor_descricao}</td>
    <td>${usuario.credencial_nome}</td>
    <td>${usuario.ativo ? "Sim" : "Não"}</td>
    <td>
      ${ possuiPermissao("USUARIO_EDITAR") ? botaoEditar : "" }
    </td>`;

  return tr;
}

function renderizarUsuarios() {

  const tbody = document.getElementById("usuarios-tbody");
  tbody.innerHTML = "";
  const usuariosPagina = paginacaoUsuarios.obterDadosDaPagina();

  for (const usuario of usuariosPagina) {
    tbody.appendChild(criarLinhaUsuario(usuario));
  }

  paginacaoUsuarios.renderizar();
}

async function buscarUsuarios() {

  const response = await fetch("/usuarios");
  if (!response.ok) {
    throw new Error("Erro ao buscar usuários.");
  }

  return await response.json();
}

async function carregarUsuarios() {
  usuarios = await buscarUsuarios();
  renderizarUsuarios();
}

paginacaoUsuarios = criarPaginacaoTabela({
  containerId: "usuarios-pagination",
  seletorQuantidade: "usuarios-qtd-registros",
  obterDados: () => filtroUsuarios.obterDadosFiltrados(),
  aoMudarPagina: () => renderizarUsuarios()
});

document.addEventListener(
  "DOMContentLoaded",
  async () => {
    try {
      await exigirPermissao("ROTA_USUARIOS");
      habilitarValidacaoEmTempoRealUsuario();
      carregarUsuarioCabecalho();
      filtroUsuarios.inicializar();
      paginacaoUsuarios.inicializar();
      await carregarCombosUsuario();
      await carregarUsuarios();
    } catch (erro) {
      console.error(erro);
      alert("Erro ao carregar usuários.");
    }
  }
);

async function abrirModalUsuario() {
  document.getElementById("modalUsuario").style.display = "flex";
}

function fecharModalUsuario() {
  limparModalUsuario();
  document.getElementById("modalUsuario").style.display = "none";
}

window.addEventListener(
  "click",
  function(event) {
    const modal = document.getElementById("modalUsuario");
    if (event.target === modal) {
      fecharModalUsuario();
    }
  }
);

document.addEventListener(
  "keydown",
  function(event) {
    if (event.key === "Escape") {
      fecharModalUsuario();
    }
  }
);

async function abrirEditarUsuario(idUsuario) {

  estadoModalUsuario.modo = "edicao";
  estadoModalUsuario.idUsuario = idUsuario;

  const response = await fetch(`/usuarios/${idUsuario}`);
  if (!response.ok) {
    alert("Erro ao carregar usuário.");
    return;
  }

  const usuario = await response.json();

  await Promise.all([
    preencherSelect(document.getElementById("usuario-tipo"), "/tipos", "id", "nome"),
    preencherSelect(document.getElementById("usuario-setor"), "/setores", "id", "descricao"),
    preencherSelect(document.getElementById("usuario-credencial"), "/credenciais", "id", "nome") ]);

  document.getElementById("modal-usuario-titulo").textContent = "Editar usuário";
  preencherModalUsuario(usuario);
  configurarModoEdicaoUsuario();
  abrirModalUsuario();
}

async function abrirNovoUsuario() {

  estadoModalUsuario.modo = "novo";
  estadoModalUsuario.idUsuario = null;
  limparModalUsuario();
  configurarModoNovoUsuario();

  document.getElementById("modal-usuario-titulo").textContent = "Novo usuário";
  document.getElementById("usuario-ativo").checked = true;

  await abrirModalUsuario();
}

function preencherModalUsuario(usuario) {

  document.getElementById("usuario-nome").value = usuario.nome ?? "";
  document.getElementById("usuario-email").value = usuario.email ?? "";
  document.getElementById("usuario-telefone").value = usuario.telefone ?? "";
  document.getElementById("usuario-tipo").value = usuario.id_tipo;
  document.getElementById("usuario-setor").value = usuario.id_setor;
  document.getElementById("usuario-credencial").value = usuario.id_credencial;
  document.getElementById("usuario-ativo").checked = usuario.ativo;
  document.getElementById("usuario-data-criacao").textContent = formatarData(usuario.data_criacao);
  document.getElementById("usuario-data-alteracao").textContent = formatarData(usuario.data_ultima_alteracao);
  document.getElementById("usuario-senha").value = "";
  document.getElementById("usuario-confirmacao-senha").value = "";

}

document.getElementById("btn-salvar-usuario").addEventListener("click", salvarUsuario);

async function salvarUsuario() {

  if (!validarFormularioUsuario()) {
    return;
  }

  if (estadoModalUsuario.modo === "novo") {
    await criarUsuario();
  } else {
    await atualizarUsuario();
  }
}

async function criarUsuario() {

  const payload = obterPayloadUsuario();
  const response = await fetch(
    "/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload) });

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail);
    return;
  }

  fecharModalUsuario();
  await carregarUsuarios();
}

function obterPayloadUsuario() {

  const alterarSenha =
    estadoModalUsuario.modo === "novo"
    || document.getElementById("usuario-alterar-senha").checked;

  return {

    nome: document.getElementById("usuario-nome").value.trim(),
    email: document.getElementById("usuario-email").value.trim(),
    telefone: document.getElementById("usuario-telefone").value.trim(),

    id_tipo: parseInt(document.getElementById("usuario-tipo").value),
    id_setor: parseInt(document.getElementById("usuario-setor").value),
    id_credencial: parseInt(document.getElementById("usuario-credencial").value),

    senha: alterarSenha
      ? document.getElementById("usuario-senha").value.trim()
      : null,

    ativo: document.getElementById("usuario-ativo").checked
  };
}

function limparErrosFormularioUsuario() {

  document.querySelectorAll("#modal-usuario .campo-invalido").forEach(
    campo => campo.classList.remove("campo-invalido"));

  document.querySelectorAll("#modal-usuario .campo-valido").forEach(
    campo => campo.classList.remove("campo-valido"));
}

function destacarCampoInvalido(campo, mensagem) {

  campo.classList.remove("campo-valido");
  campo.classList.add("campo-invalido");

  campo.focus();
  alert(mensagem);

  return false;
}


function obterResultadoValidacao(campo) {

  if (!campo.checkValidity()) {
    return false;
  }

  const valor = campo.value.trim();

  switch (campo.dataset.validacao) {

    case "obrigatorio":
      return valor !== "";

    default:
      return true;
  }
}

function validarCampo(campo) {

  if (!campo) {
    console.error("Campo nulo!");
    return false;
  }

  const valido = obterResultadoValidacao(campo);

  if (valido) {
    marcarCampoValido(campo);
    return true;
  }

  destacarCampoInvalido(
    campo,
    campo.validationMessage || "Campo inválido."
  );

  return false;
}

function validarCampoObrigatorio(campo, mensagem = null) {

  if (validarCampo(campo)) {
    return true;
  }

  alert(mensagem ?? campo.validationMessage);

  campo.focus();
  return false;
}

function validarCampoEmTempoReal(campo) {
  validarCampo(campo);
}

function habilitarValidacaoEmTempoRealUsuario() {

  const campos = document.querySelectorAll(
    "#modal-usuario input," +
    "#modal-usuario select," +
    "#modal-usuario textarea");

  campos.forEach(campo => {
    
    if (campo.dataset.validacao === "true") {
      return;
    }

    campo.dataset.validacao = "true";
    const evento = (campo.tagName === "SELECT") ? "change" : "input";

    campo.addEventListener(evento, () => validarCampoEmTempoReal(campo));
  });
}

function validarFormularioUsuario() {

  limparErrosFormularioUsuario();

  const campoNome = document.getElementById("usuario-nome");
  const campoEmail = document.getElementById("usuario-email");
  const campoTipo = document.getElementById("usuario-tipo");
  const campoSetor = document.getElementById("usuario-setor");
  const campoCredencial = document.getElementById("usuario-credencial");
  const campoSenha = document.getElementById("usuario-senha");
  const campoConfirmacaoSenha = document.getElementById("usuario-confirmacao-senha");

  if (!validarCampoObrigatorio(campoNome)) {
    return false;
  }

  if (!validarCampoObrigatorio(campoEmail)) {
    return false;
  }

  if (!validarCampoObrigatorio(campoTipo)) {
    return false;
  }

  if (!validarCampoObrigatorio(campoSetor)) {
    return false;
  }

  if (!validarCampoObrigatorio(campoCredencial)) {
    return false;
  }

  const validarSenha =
    estadoModalUsuario.modo === "novo" ||
    document.getElementById("usuario-alterar-senha").checked;

  if (!validarSenha) {
    return true;
  }

  if (!validarCampoObrigatorio(campoSenha)) {
    return false;
  }

  if (!validarCampoObrigatorio(campoConfirmacaoSenha)) {
    return false;
  }

  if (!senhaForte(campoSenha.value)) {
    alert("A senha deve possuir ao menos 8 caracteres, letra maiúscula, letra minúscula, número e símbolo.");
    marcarCampoInvalido(campoSenha);
    campoSenha.focus();
    return false;
  }

  if (campoSenha.value !== campoConfirmacaoSenha.value) {

    destacarCampoInvalido(
      campoConfirmacaoSenha,
      "As senhas não coincidem."
    );

    return false;
  }

  return true;
}

async function atualizarUsuario() {

  const payload = obterPayloadUsuario();

  const response = await fetch(`/usuarios/${estadoModalUsuario.idUsuario}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail);
    return;
  }

  fecharModalUsuario();
  await carregarUsuarios();
}

function limparModalUsuario() {

  document.getElementById("usuario-nome").value = "";
  document.getElementById("usuario-email").value = "";
  document.getElementById("usuario-telefone").value = "";
  document.getElementById("usuario-tipo").value = "";
  document.getElementById("usuario-setor").value = "";
  document.getElementById("usuario-credencial").value = "";
  document.getElementById("usuario-senha").value = "";
  document.getElementById("usuario-confirmacao-senha").value = "";
  document.getElementById("usuario-ativo").checked = true;
  document.getElementById("usuario-data-criacao").textContent = "—";
  document.getElementById("usuario-data-alteracao").textContent = "—";

}

function configurarModoNovoUsuario() {
  document.getElementById("container-alterar-senha").style.display = "none";
  document.getElementById("usuario-alterar-senha").checked = false;
  document.getElementById("usuario-senha").disabled = false;
  document.getElementById("usuario-confirmacao-senha").disabled = false;
}

function configurarModoEdicaoUsuario() {
  document.getElementById("container-alterar-senha").style.display = "flex";
  document.getElementById("usuario-alterar-senha").checked = false;
  document.getElementById("usuario-senha").disabled = true;
  document.getElementById("usuario-confirmacao-senha").disabled = true;
  atualizarEstadoAlteracaoSenha();
}

function atualizarEstadoAlteracaoSenha() {

  const alterarSenha =
    document.getElementById("usuario-alterar-senha").checked;

  const campoSenha =
    document.getElementById("usuario-senha");

  const campoConfirmacaoSenha =
    document.getElementById("usuario-confirmacao-senha");

  campoSenha.disabled = !alterarSenha;
  campoConfirmacaoSenha.disabled = !alterarSenha;

  if (alterarSenha) {

    campoSenha.focus();
    return;
  }

  campoSenha.value = "";
  campoConfirmacaoSenha.value = "";

  campoSenha.classList.remove(
    "campo-valido",
    "campo-invalido"
  );

  campoConfirmacaoSenha.classList.remove(
    "campo-valido",
    "campo-invalido"
  );
}

async function preencherSelect(select, endpoint, campoId, campoDescricao) {

  const resposta = await fetch(endpoint);

  if (!resposta.ok) {
    throw new Error(`Erro ao carregar ${endpoint}.`);
  }

  const registros = await resposta.json();

  select.innerHTML = "";

  const opcaoPadrao = document.createElement("option");
  opcaoPadrao.value = "";
  opcaoPadrao.textContent = "Selecione...";
  select.appendChild(opcaoPadrao);

  for (const registro of registros) {

    const option = document.createElement("option");

    option.value = registro[campoId];
    option.textContent = registro[campoDescricao];

    select.appendChild(option);
  }
}

async function carregarCombosUsuario() {

  await Promise.all([

    preencherSelect(document.getElementById("usuario-tipo"),
      "/tipos", "id", "nome"),

    preencherSelect(document.getElementById("usuario-setor"),
      "/setores", "id", "descricao"),

    preencherSelect(document.getElementById("usuario-credencial"),
      "/credenciais", "id", "nome")

  ]);
}
