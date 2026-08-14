const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const loginButton = document.getElementById("login-button");
const mensagemErro = document.getElementById("mensagem-erro");


document.addEventListener(
  "DOMContentLoaded",
  async () => {

    const response = await fetch("/eu");

    if (!response.ok) {
      return;
    }

    const usuario = await response.json();

    window.location.href =
      PAGES_BASE_URL +
      (usuario.permissoes.includes("ROTA_MAIN")
        ? ROTA_MAIN
        : ROTA_ACESSO_NEGADO);
  }
);


form.addEventListener("submit", async (event) => {

  event.preventDefault();

  mensagemErro.innerText = "";
  mensagemErro.style.display = "none";

  loginButton.disabled = true;
  loginButton.innerText = "Entrando...";

  try {

    const response = await fetch(
      PAGES_BASE_URL + ROTA_LOGIN, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: emailInput.value.trim(),
          senha: senhaInput.value
        })
      }
    );

    const data = await response.json();
    if (!response.ok) {
      mensagemErro.innerText = data.detail || "Falha no login.";
      mensagemErro.style.display = "block";
      return;
    }

    localStorage.setItem("USUARIO_LOGADO", JSON.stringify(data.usuario));

    window.location.href = PAGES_BASE_URL + (data.usuario.permissoes.includes("ROTA_MAIN") ?
      ROTA_MAIN : ROTA_ACESSO_NEGADO);

  } catch (error) {
    console.error(error);
    mensagemErro.innerText = "Erro de comunicação com o servidor.";

  } finally {
    loginButton.disabled = false;
    loginButton.innerText = "Entrar";
  }
});
