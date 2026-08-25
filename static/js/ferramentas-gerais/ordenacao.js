let campoOrdenacao = "id";
let ordemCrescente = false;

function ordenar(lista) {

  const listaOrdenada = [...lista];

  listaOrdenada.sort((a, b) => {

    let valorA = a [campoOrdenacao];
    let valorB = b [campoOrdenacao];

    if (valorA == null) { 
      valorA = "";
    }

    if (valorB == null) {
      valorB = "";
    }

    if (typeof valorA === "string") {
      valorA = valorA.toUpperCase();
    }

    if (typeof valorB === "string") {
      valorB = valorB.toUpperCase();
    }

    if (valorA < valorB) {
      return ordemCrescente ? -1 : 1;
    }

    if (valorA > valorB) {
      return ordemCrescente ? 1 : -1;
    }

    return 0;
  });

  return listaOrdenada;
}

function ordenarPor(campo) {
  if (campoOrdenacao === campo) {
    ordemCrescente = !ordemCrescente;

  } else {
    campoOrdenacao = campo;
    ordemCrescente = true;
  }

  paginaAtual = 1;
  renderizarAutorizacoes();
}
