function obterUsuariosFiltrados() {

  const textoBusca =
    document
      .getElementById(
        "filtro-usuarios"
      )
      .value
      .toLowerCase();

  const filtroAtivo =
    document
      .getElementById(
        "filtro-ativo"
      )
      .value;

  return usuarios.filter(
    usuario => {

      const correspondeTexto =

        usuario.nome
          .toLowerCase()
          .includes(
            textoBusca
          )

        ||

        usuario.email
          .toLowerCase()
          .includes(
            textoBusca
          );

      const correspondeAtivo =

        filtroAtivo === ""

        ||

        String(
          usuario.ativo
        ) === filtroAtivo;

      return (
        correspondeTexto
        &&
        correspondeAtivo
      );
    }
  );
}
