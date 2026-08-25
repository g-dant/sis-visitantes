function obterPaginaAtual(lista, paginaAtual, registrosPorPagina) {

  if (registrosPorPagina === -1) {
    return lista;
  }

  const inicio = (paginaAtual - 1) * registrosPorPagina;
  const fim = inicio + registrosPorPagina;

  return lista.slice(inicio, fim);
}

function obterTotalPaginas(quantidadeRegistros, registrosPorPagina) {

  if (registrosPorPagina === -1) {
    return 1;
  }

  return Math.ceil(quantidadeRegistros / registrosPorPagina);
}

function renderizarPaginacao({
  containerId,
  paginaAtual,
  registrosPorPagina,
  quantidadeRegistros,
  aoVoltar,
  aoAvancar,
  aoSelecionarPagina
}) {

  const container = document.getElementById(containerId);

  if (!container) {
    return;
  }

  container.innerHTML = "";

  if (registrosPorPagina === -1) {
    return;
  }

  const totalPaginas = obterTotalPaginas(quantidadeRegistros, registrosPorPagina);
  const anterior = document.createElement("button");

  anterior.textContent = "«";
  anterior.disabled = paginaAtual === 1;
  anterior.onclick = aoVoltar;

  container.appendChild(anterior);

  for (let i = 1; i <= totalPaginas; i++) {

    const botao = document.createElement("button");
    botao.textContent = i;

    if (i === paginaAtual) {
      botao.classList.add("active");
    }

    botao.onclick = () => {
      aoSelecionarPagina(i);
    };

    container.appendChild(botao);
  }

  const proxima = document.createElement("button");

  proxima.textContent = "»";
  proxima.disabled = paginaAtual === totalPaginas;
  proxima.onclick = aoAvancar;
  container.appendChild(proxima);
}

function criarPaginacaoTabela({
  containerId,
  seletorQuantidade,
  obterDados,
  aoMudarPagina
}) {

  let paginaAtual = 1;
  let registrosPorPagina = 10;

  function obterDadosDaPagina() {
    const dados = obterDados();
    return obterPaginaAtual(dados, paginaAtual, registrosPorPagina);
  }

  function renderizar() {

    const dados = obterDados();
    const quantidadeRegistros = dados.length;
    const totalPaginas = obterTotalPaginas(quantidadeRegistros, registrosPorPagina);

    if (paginaAtual > totalPaginas && totalPaginas > 0) {
      paginaAtual = totalPaginas;
    }

    renderizarPaginacao({
      containerId,
      paginaAtual,
      registrosPorPagina,
      quantidadeRegistros,

      aoVoltar: () => {
        if (paginaAtual > 1) {
          paginaAtual--;
          aoMudarPagina();
        }
      },

      aoAvancar: () => {
        if (paginaAtual < totalPaginas) {
          paginaAtual++;
          aoMudarPagina();
        }
      },

      aoSelecionarPagina: pagina => {
        paginaAtual = pagina;
        aoMudarPagina();
      }
    });
  }

  function alterarQuantidade() {

    const elemento = document.getElementById(seletorQuantidade);

    registrosPorPagina = parseInt(elemento.value);
    paginaAtual = 1;
    aoMudarPagina();
  }

  function reiniciar() {
    paginaAtual = 1;
    aoMudarPagina();
  }

  function inicializar() {

    const elemento = document.getElementById(seletorQuantidade);

    if (elemento) {
      elemento.addEventListener("change", alterarQuantidade);
    }
  }

  return {
    obterDadosDaPagina,
    renderizar,
    reiniciar,
    inicializar
  };
}
