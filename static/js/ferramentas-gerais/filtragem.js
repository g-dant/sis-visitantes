function filtrarPorTexto(lista, texto, campos) {

  const textoNormalizado = texto.trim().toLowerCase();

  if (!textoNormalizado) {
    return lista;
  }

  return lista.filter(
    item =>
      campos.some(
        campo =>
          String(item[campo] ?? "")
            .toLowerCase()
            .includes(textoNormalizado)
      )
  );
}


function criarFiltroTabela({
  obterDados,
  campoTextoId,
  camposTexto,
  filtros = [],
  aoFiltrar
}) {

  function obterDadosFiltrados() {

    let resultado = obterDados();

    const campoTexto =
      document.getElementById(campoTextoId);

    if (campoTexto) {

      resultado = filtrarPorTexto(
        resultado,
        campoTexto.value,
        camposTexto
      );
    }

    for (const filtro of filtros) {

      const elemento =
        document.getElementById(filtro.elementoId);

      if (!elemento) {
        continue;
      }

      const valor = elemento.value;

      resultado = resultado.filter(
        registro =>
          filtro.aplicar(
            registro,
            valor
          )
      );
    }

    return resultado;
  }


  function inicializar() {

    const campoTexto =
      document.getElementById(campoTextoId);

    if (campoTexto) {

      campoTexto.addEventListener(
        "input",
        aoFiltrar
      );
    }

    for (const filtro of filtros) {

      const elemento =
        document.getElementById(filtro.elementoId);

      if (!elemento) {
        continue;
      }

      elemento.addEventListener(
        "change",
        aoFiltrar
      );
    }
  }


  return {
    obterDadosFiltrados,
    inicializar
  };
}
