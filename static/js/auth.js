async function buscarUsuarioLogado() {

  const response = await fetch("/eu");

  if (response.status === 401) {
    window.location.href = "/";
    return null;
  }

  if (!response.ok) {
    throw new Error("Erro ao obter usuário logado.");
  }

  return await response.json();
}


async function exigirPermissao(codigoPermissao) {

  const usuario = await buscarUsuarioLogado();

  if (usuario == null) {
    return;
  }

  if (!usuario.permissoes.includes(codigoPermissao)) {

    window.location.href = "/pages/acesso-negado";
    return null;
  }

  return usuario;
}


function obterUsuarioLogado() {

  const usuario = localStorage.getItem(
    USUARIO_LOGADO_KEY);

  if (usuario == null) {
    return null;
  }

  return JSON.parse(usuario);
}


function possuiPermissao(codigoPermissao) {

  const usuario = obterUsuarioLogado();

  if (usuario == null) {
    return false;
  }

  return usuario.permissoes.includes(codigoPermissao);
}

