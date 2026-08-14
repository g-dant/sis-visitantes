function carregarUsuarioCabecalho() {

  usuarioLogado = obterUsuarioLogado();

  if (usuarioLogado == null) {
    localStorage.removeItem(TOKEN_KEY);
    window.location.href = "/";
    return;
  }

  document.getElementById("header-usuario-nome").innerText = usuarioLogado.nome;
  document.getElementById("header-usuario-credencial").innerText = usuarioLogado.credencial;
  document.getElementById("header-usuario-setor").innerText = usuarioLogado.setor_codigo;
}
