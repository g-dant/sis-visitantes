let visitantes = [];

const estadoModalVisitante = {
  modo: "novo",
  idVisitante: null
};

let filtroVisitantes = criarFiltroTabela({

  obterDados: () => visitantes,
  campoTextoId: "filtro-visitantes",
  camposTexto: [
      "nome",
      "cpf",
      "rg",
      "email",
      "celular",
      "empresa_nome"
  ],

  filtros: [{
    elementoId: "filtro-visitantes-ativo",
    aplicar: (visitante, valor) =>
      valor === "" ||
      String(visitante.ativo) === valor
  }],

  aoFiltrar: () => paginacaoVisitantes.reiniciar()
});


let paginacaoVisitantes = criarPaginacaoTabela({
  containerId: "visitantes-pagination",
  seletorQuantidade: "visitantes-qtd-registros",
  obterDados: () => filtroVisitantes.obterDadosFiltrados(),
  aoMudarPagina: () => renderizarVisitantes()
});

function criarLinhaVisitante(visitante) {

  const tr = document.createElement("tr");
  let botoesAcoes = "";
  if (possuiPermissao("VISITANTE_EDITAR")) {

    botoesAcoes += `
      <button
        class="btn btn-primary"
        title="Editar visitante"
        onclick='abrirModalNovoVisitante(
          "Editar visitante",
          {
            id: ${visitante.id},
            nome: ${JSON.stringify(visitante.nome)},
            email: ${JSON.stringify(visitante.email)},
            telefone: ${JSON.stringify(visitante.celular)},
            rg: ${JSON.stringify(visitante.rg)},
            cpf: ${JSON.stringify(visitante.cpf)},
            empresa: ${visitante.id_empresa},
            ativo: ${visitante.ativo}
          }
        )'>
        <i class="fa-solid fa-pen"></i>
      </button>`;
  }

  if (possuiPermissao("VISITANTE_EXCLUIR") && visitante.pode_excluir) {

    botoesAcoes += `
      <button
        class="btn btn-danger"
        title="Excluir visitante"
        onclick="excluirVisitante(${visitante.id})">
        <i class="fa-solid fa-trash"></i>
      </button>`;
  }

  tr.innerHTML = `

    <td>${visitante.nome ?? ""}</td>
    <td style="text-align: center;">${ formatarCpf(visitante.cpf) }</td>
    <td style="text-align: center;">${visitante.rg ?? ""}</td>
    <td>${visitante.email ?? ""}</td>
    <td style="text-align: center;"">${visitante.celular ?? ""}</td>
    <td>${visitante.empresa_nome ?? ""}</td>
    <td style="text-align: center;">${visitante.ativo ? "Sim" : "Não"}</td>
    <td style="text-align: center;">
      ${botoesAcoes}
    </td>`;

  return tr;
}


function renderizarVisitantes() {

  const tbody = document.getElementById("visitantes-tbody");
  tbody.innerHTML = "";
  const visitantesPagina = paginacaoVisitantes.obterDadosDaPagina();

  for (const visitante of visitantesPagina) {
    tbody.appendChild(criarLinhaVisitante(visitante));
  }

  paginacaoVisitantes.renderizar();
}


async function buscarVisitantes() {

  const response = await fetch("/visitantes");

  if (!response.ok) {
    throw new Error("Erro ao buscar visitantes.");
  }

  return await response.json();
}


async function carregarVisitantes() {
  visitantes = await buscarVisitantes();
  renderizarVisitantes();
}

function abrirModalCadastroVisitantes() {
  const modal = document.getElementById("modalCadastroVisitantes");
  modal.style.display = "flex";
}

function fecharModalCadastroVisitantes() {
  const modal = document.getElementById("modalCadastroVisitantes");
  modal.style.display = "none";
}

document.addEventListener(
  "DOMContentLoaded",
  async () => {
    try {

      filtroVisitantes.inicializar();
      paginacaoVisitantes.inicializar();

      await carregarVisitantes();

    } catch (erro) {
      console.error(erro);
      alert("Erro ao carregar visitantes");
    }
  }
);

async function abrirModalNovoVisitante(titulo = "Novo visitante", dados = {}) {

  limparModalNovoVisitante();

  estadoModalVisitante.modo = (dados.id != null) ? "editar" : "novo";
  estadoModalVisitante.idVisitante = dados.id;

  document.getElementById("modal-novo-visitante-titulo").textContent = titulo;

  await carregarEmpresasVisitante();

  document.getElementById("novo-visitante-nome").value = dados.nome ?? "";
  document.getElementById("novo-visitante-email").value = dados.email ?? "";
  document.getElementById("novo-visitante-telefone").value = dados.telefone ?? "";
  document.getElementById("novo-visitante-rg").value = dados.rg ?? "";
  document.getElementById("novo-visitante-cpf").value = dados.cpf ?? "";
  document.getElementById("novo-visitante-empresa").value = dados.empresa ?? "";
  document.getElementById("novo-visitante-ativo").value = dados.ativo ?? true;

  const modal = document.getElementById("modalNovoVisitante");
  modal.style.display = "flex";

  inicializarValidacaoVisitante();
}

function limparModalNovoVisitante() {

  for (let idCampo of ["novo-visitante-nome", "novo-visitante-email",
	               "novo-visitante-telefone", "novo-visitante-rg",
	               "novo-visitante-cpf", "novo-visitante-empresa",
	               "novo-visitante-ativo"]) {

    document.getElementById(idCampo).value = "";
  }

  document.querySelectorAll("#modalNovoVisitante .campo-invalido").forEach(
    campo => campo.classList.remove("input-invalido"));
}


function fecharModalNovoVisitante() {
  const modal = document.getElementById("modalNovoVisitante");
  modal.style.display = "none";
}

function obterCamposObrigatoriosVisitante() {
  return [
    document.getElementById("novo-visitante-nome"),
    document.getElementById("novo-visitante-cpf"),
    document.getElementById("novo-visitante-empresa")
  ];
}


function validarCampoObrigatorioVisitante(campo) {

  const valor = campo.value.trim();

  if (valor === "") {
    campo.classList.add("input-invalido");
    return false;
  }

  campo.classList.remove("input-invalido");
  return true;
}


function validarFormularioVisitante() {

  const campos = obterCamposObrigatoriosVisitante();
  let valido = true;

  for (const campo of campos) {
    if (!validarCampoObrigatorioVisitante(campo)) {
      valido = false;
    }
  }

  return valido;
}

function atualizarEstadoBotaoSalvarVisitante() {

  const botao = document.getElementById("btn-salvar-novo-visitante");
  const campos = obterCamposObrigatoriosVisitante();
  const valido = campos.every(campo => campo.value.trim() !== "");

  botao.setAttribute("aria-disabled", String(!valido));
  botao.classList.toggle("btn-desabilitado", !valido);
}

function inicializarValidacaoVisitante() {

  const campos = obterCamposObrigatoriosVisitante();
  for (const campo of campos) {

    campo.addEventListener("input", () => {
      validarCampoObrigatorioVisitante(campo);
      atualizarEstadoBotaoSalvarVisitante();
    });
  }

  atualizarEstadoBotaoSalvarVisitante();
}

async function carregarEmpresasVisitante() {

  const select = document.getElementById("novo-visitante-empresa");

  const response = await fetch("/empresas", {
    headers: { Authorization: `Bearer ${ obterToken() }` } });

  if (!response.ok) {
    throw new Error("Erro ao carregar empresas.");
  }

  const empresas = await response.json();
  select.innerHTML = "";

  const opcaoPadrao = document.createElement("option");

  opcaoPadrao.value = "";
  opcaoPadrao.textContent = "Selecione uma empresa";

  select.appendChild(opcaoPadrao);

  for (const empresa of empresas) {

    const opcao = document.createElement("option");

    opcao.value = empresa.id;
    opcao.textContent = empresa.nome;

    select.appendChild(opcao);
  }
}

async function salvarNovoVisitante() {

  if (!validarFormularioVisitante()) {
    atualizarEstadoBotaoSalvarVisitante();
    return;
  }

  const payload = {

    nome: document.getElementById("novo-visitante-nome").value.trim(),

    email: document.getElementById("novo-visitante-email").value.trim(),

    celular: document.getElementById("novo-visitante-telefone").value.trim(),

    rg: document.getElementById("novo-visitante-rg").value.trim(),

    cpf: document.getElementById("novo-visitante-cpf").value.trim(),

    id_empresa: Number(document.getElementById("novo-visitante-empresa").value),

    ativo: document.getElementById("novo-visitante-ativo").checked

  };


  const emEdicao = estadoModalVisitante.modo === "editar";
  const url = emEdicao
      ? `/visitantes/${estadoModalVisitante.idVisitante}`
      : "/visitantes";
  
  const metodo = emEdicao ? "PUT" : "POST";
  const response = await fetch(url, {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${obterToken()}`
    },
    body: JSON.stringify(payload)
  });


  if (!response.ok) {
  
    const erro = await response.json();
    let mensagem = "Erro ao adicionar visitante.";
  
    if (Array.isArray(erro.detail)) {
      mensagem = erro.detail.map(item => item.msg).join("\n");
    } else if (erro.detail) {
      mensagem = erro.detail;
    }
  
    alert(mensagem);
    return;
  }


  fecharModalNovoVisitante();
  alert("Visitante adicionado com sucesso");

  await carregarVisitantes();
}

async function carregarEmpresasVisitante() {

  const select = document.getElementById("novo-visitante-empresa");

  try {

    const response = await fetch("/empresas");
    if (!response.ok) {
      throw new Error("Erro ao carregar empresas.");
    }

    const empresas = await response.json();

    select.innerHTML = `
      <option value="">
        Selecione uma empresa
      </option>`;

    empresas.forEach(empresa => {

      const option = document.createElement("option");

      option.value = String(empresa.id);
      option.textContent = empresa.nome;

      select.appendChild(option);

    });

  } catch (erro) {
    console.error("Erro ao carregar empresas:", erro);
  }
}

async function excluirVisitante(idVisitante) {

  if (!confirm("Deseja realmente excluir este visitante?")) {
    return;
  }

  try {

    const response = await fetch(`/visitantes/${idVisitante}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${ obterToken() }` }
    });

    if (!response.ok) {

      const erro = await response.json();
      let mensagem = "Erro ao excluir visitante.";

      if (Array.isArray(erro.detail)) {
        mensagem = erro.detail.map(item => item.msg).join("\n");
      } else if (erro.detail) {
        mensagem = erro.detail;
      }

      alert(mensagem);
      return;
    }

    alert("Visitante excluído com sucesso");
    await carregarVisitantes();

  } catch (erro) {
    console.error("Erro ao excluir visitante:", erro);
    alert("Erro ao excluir visitante.");
  }
}
