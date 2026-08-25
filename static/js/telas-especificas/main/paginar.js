let paginaAtual = 1;
let registrosPorPagina = 10;
let autorizacoes = [];

function obterItensPaginaAtual(lista) {

  if (registrosPorPagina === -1) {
    return lista;
  }

  const inicio = (paginaAtual - 1) * registrosPorPagina;
  const fim = inicio + registrosPorPagina;

  return lista.slice(inicio, fim);
}

function irParaPagina(numeroPagina) {
  paginaAtual = numeroPagina;
  carregarAutorizacoes();
}

function paginaAnterior() {
  if (paginaAtual > 1) {
    paginaAtual--;
    renderizarAutorizacoes();
  }
}

function paginaProxima() {
  const totalPaginas = Math.ceil(autorizacoes.length / registrosPorPagina);
  if (paginaAtual < totalPaginas) {
    paginaAtual++;
    renderizarAutorizacoes();
  }
}

function alterarQuantidadeRegistros() {
  registrosPorPagina = parseInt(document.getElementById("qtd-registros").value);
  paginaAtual = 1;
  renderizarAutorizacoes();
}

function renderizarPaginacao() {

  const container = document.getElementById("pagination");
  container.innerHTML = "";

  if (registrosPorPagina === -1) {
    return;
  }

  const totalPaginas = Math.ceil(obterItensFiltrados().length / registrosPorPagina);
  const anterior = document.createElement("button");

  anterior.textContent = "«";
  anterior.disabled = paginaAtual === 1;
  anterior.onclick = paginaAnterior;
  container.appendChild(anterior);

  for (let i = 1; i <= totalPaginas; i++) {

    const btn = document.createElement("button");
    btn.textContent = i;

    if (i === paginaAtual) {
      btn.classList.add("active");
    }

    btn.onclick = () => {
      paginaAtual = i;
      renderizarAutorizacoes();
    };

    container.appendChild(btn);
  }

  const proxima = document.createElement("button");

  proxima.textContent = "»";
  proxima.disabled = paginaAtual === totalPaginas;
  proxima.onclick = paginaProxima;

  container.appendChild(proxima);
}
