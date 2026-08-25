const TOKEN_KEY = "token";
const USUARIO_LOGADO_KEY = "USUARIO_LOGADO";

const PAGES_BASE_URL = "/pages";
const ROTA_LOGIN = "/login";
const ROTA_MAIN = "/main";
const ROTA_ACESSO_NEGADO = "/acesso-negado";

function obterToken() {
  return localStorage.getItem(TOKEN_KEY);
}
