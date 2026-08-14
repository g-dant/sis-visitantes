let usuariosPaginaAtual = 1;

let usuariosRegistrosPorPagina = 10;

function obterUsuariosPaginaAtual(
  lista
) {

  if (
    usuariosRegistrosPorPagina === -1
  ) {
    return lista;
  }

  const inicio =
    (usuariosPaginaAtual - 1)
    * usuariosRegistrosPorPagina;

  const fim =
    inicio
    + usuariosRegistrosPorPagina;

  return lista.slice(
    inicio,
    fim
  );
}

function usuariosPaginaAnterior() {

  if (
    usuariosPaginaAtual > 1
  ) {

    usuariosPaginaAtual--;

    renderizarUsuarios();
  }
}

function usuariosPaginaProxima() {

  const totalPaginas =
    Math.ceil(
      obterUsuariosFiltrados().length
      / usuariosRegistrosPorPagina
    );

  if (
    usuariosPaginaAtual
    < totalPaginas
  ) {

    usuariosPaginaAtual++;

    renderizarUsuarios();
  }
}

function alterarQuantidadeUsuarios() {

  usuariosRegistrosPorPagina =
    parseInt(
      document.getElementById(
        "usuarios-qtd-registros"
      ).value
    );

  usuariosPaginaAtual = 1;

  renderizarUsuarios();
}

function renderizarPaginacaoUsuarios() {

  const container =
    document.getElementById(
      "usuarios-pagination"
    );

  container.innerHTML = "";

  if (
    usuariosRegistrosPorPagina === -1
  ) {
    return;
  }

  const totalPaginas =
    Math.ceil(
      obterUsuariosFiltrados().length
      / usuariosRegistrosPorPagina
    );

  const anterior =
    document.createElement(
      "button"
    );

  anterior.textContent = "«";

  anterior.disabled =
    usuariosPaginaAtual === 1;

  anterior.onclick =
    usuariosPaginaAnterior;

  container.appendChild(
    anterior
  );

  for (
    let i = 1;
    i <= totalPaginas;
    i++
  ) {

    const botao =
      document.createElement(
        "button"
      );

    botao.textContent = i;

    if (
      i === usuariosPaginaAtual
    ) {

      botao.classList.add(
        "active"
      );
    }

    botao.onclick = () => {

      usuariosPaginaAtual = i;

      renderizarUsuarios();
    };

    container.appendChild(
      botao
    );
  }

  const proxima =
    document.createElement(
      "button"
    );

  proxima.textContent = "»";

  proxima.disabled =
    usuariosPaginaAtual
    === totalPaginas;

  proxima.onclick =
    usuariosPaginaProxima;

  container.appendChild(
    proxima
  );
}
