let filtroBusca = "";
let filtroStatus = "ATIVOS_E_PENDENTES";
let filtroSetor = "TODOS";
let filtroData = "";

document.getElementById("input-busca-texto").addEventListener("input", alterarBusca);
document.getElementById("select-status").addEventListener("change", alterarFiltroStatus);
document.getElementById("select-setor").addEventListener("change", alterarFiltroSetor);
document.getElementById("input-data").addEventListener("change", alterarFiltroData);

function alterarBusca() {
  filtroBusca = document.getElementById("input-busca-texto").value.trim().toLowerCase();
  paginaAtual = 1;
  renderizarAutorizacoes();
}

function alterarFiltroStatus() {
  filtroStatus = document.getElementById("select-status").value;
  paginaAtual = 1;
  renderizarAutorizacoes();
}

function alterarFiltroSetor() {
  filtroSetor = document.getElementById("select-setor").value;
  paginaAtual = 1;
  renderizarAutorizacoes();
}

function alterarFiltroData() {
  filtroData = document.getElementById("input-data").value;
  paginaAtual = 1;
  renderizarAutorizacoes();
}

async function carregarStatus() {

  const response = await fetch("/autorizacoes-consulta/status-exibicao");

  if (!response.ok) {
    return;
  }

  const listaStatusAutorizacao = await response.json();
  const select = document.getElementById("select-status");
  select.innerHTML = `
    <option value="ATIVOS_E_PENDENTES">Ativos e Pendentes</option>
    <option value="TODOS">TODOS (ativos E INATIVOS)</option>
  `;

  for (const item of listaStatusAutorizacao) {
    select.innerHTML += `<option value="${item.status_exibicao}">${item.status_exibicao}</option>`;
  }
}

async function carregarSetores() {

  const response = await fetch("/setores");
  if (!response.ok) {
    return;
  }

  const listaSetores =
    await response.json();

  const select = document.getElementById("select-setor");

  select.innerHTML = `
    <option value="TODOS">
      Todos Setores
    </option>
  `;

  for (const setor of listaSetores) {
    select.innerHTML += `
      <option value="${setor.codigo}">
        ${setor.codigo} - ${setor.descricao}
      </option>
    `;
  }
}

function buscaTextual(lista) {
  if (!filtroBusca) {
    return lista;
  }

  return lista.filter(
    autorizacao => {

      const nome = (autorizacao.visitante_nome || "").toLowerCase();
      const cpf = (autorizacao.cpf || "").toLowerCase();
      const empresa = (autorizacao.empresa_nome || "").toLowerCase();

      return (nome.includes(filtroBusca) ||
        cpf.includes(filtroBusca) ||
        empresa.includes(filtroBusca)
      );
    }
  );
}

function buscaStatus(lista) {
  if ((filtroStatus !== "TODOS") && (filtroStatus !== "ATIVOS_E_PENDENTES")) {
    lista = lista.filter(autorizacao => 
      autorizacao.status_exibicao === filtroStatus);
  } else if (filtroStatus === "ATIVOS_E_PENDENTES") {
    lista = lista.filter(autorizacao => 
      (autorizacao.status_exibicao !== "Revogada") && (autorizacao.status_exibicao !== "Expirada"));
  }
  return lista;
}

function buscaSetor(lista) {

  if (filtroSetor === "TODOS") {
    return lista;
  }

  return lista.filter(autorizacao => 
    autorizacao.setor_solicitante_codigo === filtroSetor);
}

function buscaData(lista) {

  if (!filtroData) {
    return lista;
  }

  return lista.filter(
    autorizacao =>
      filtroData >= autorizacao.primeiro_dia &&
      filtroData <= autorizacao.ultimo_dia
  );
}

function obterItensFiltrados() {
  let lista = autorizacoes;

  lista = buscaTextual(lista);
  lista = buscaStatus(lista);
  lista = buscaSetor(lista);
  lista = buscaData(lista);

  lista = ordenar(lista);

  return lista;
}
