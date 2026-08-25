const estadoEditarUsuario = {

  idUsuario: null,
  emailOriginal: "",
  nome: "",
  credencial: "",
  setor: "",
  editandoEmail: false,
  editandoSenha: false
};


function atualizarEstadoBotao() {

  const email = document.getElementById("editar-usuario-email").value;
  const senha = document.getElementById("editar-usuario-senha").value;
  const confirmarSenha = document.getElementById("editar-usuario-confirmar-senha").value;
  const emailAlterado = (email !== estadoEditarUsuario.emailOriginal);
  const emailOk = !emailAlterado || emailValido(email);
  const senhaVazia = (senha === "") && (confirmarSenha === "");
  const senhaOk = (senha !== "") && (senha === confirmarSenha) && senhaForte(senha);

  limparValidacaoCampo("editar-usuario-email", "erro-email");
  limparValidacaoCampo("editar-usuario-senha", "erro-senha");
  limparValidacaoCampo("editar-usuario-confirmar-senha", "erro-confirmar-senha");

  if (emailAlterado) {
    if (emailValido(email)) {
      marcarCampoValido("editar-usuario-email");

    } else {
      marcarCampoInvalido(
	"editar-usuario-email", 
	"erro-email", 
	"E-mail inválido.");
    }
  }

  if (senha !== "") {
    if (senhaForte(senha)) {
      marcarCampoValido("editar-usuario-senha");
    } else {
      marcarCampoInvalido("editar-usuario-senha", "erro-senha", 
        "Senha deve ter ao menos 8 caracteres com letra maiúscula, minúscula, número e símbolo");
    }
  }

  if (confirmarSenha !== "") {
    if (senha === confirmarSenha) {
      marcarCampoValido("editar-usuario-confirmar-senha");
    } else {
      marcarCampoInvalido(
	"editar-usuario-confirmar-senha",
	"erro-confirmar-senha",
	"As senhas não coincidem.");
    }
  }

  const habilitar = emailOk && (emailAlterado || senhaOk) && (senhaVazia || senhaOk);
  document.getElementById("btn-atualizar-usuario").disabled = !habilitar;
}

async function abrirModalEditarUsuario() {
  limparModalEditarUsuario();
  await carregarDadosUsuario();
  document.getElementById("modal-editar-usuario").classList.remove("oculto");
  document.getElementById("modal-editar-usuario").classList.add("aberto");
  atualizarEstadoBotao();
}

function fecharModalEditarUsuario() {
  document.getElementById("modal-editar-usuario").classList.remove("aberto");
  document.getElementById("modal-editar-usuario").classList.add("oculto");
}

function limparModalEditarUsuario() {

  document.getElementById("editar-usuario-email").disabled = true;
  document.getElementById("editar-usuario-senha").disabled = true;
  document.getElementById("editar-usuario-senha").value = "";
  document.getElementById("editar-usuario-confirmar-senha").disabled = true;
  document.getElementById("editar-usuario-confirmar-senha").value = "";

  estadoEditarUsuario.editandoEmail = false;
  estadoEditarUsuario.editandoSenha = false;

  document.getElementById("erro-email").textContent = "";
  document.getElementById("erro-senha").textContent = "";
  document.getElementById("erro-confirmar-senha").textContent = "";

  document.getElementById("editar-usuario-email").classList.remove("input-invalido", "input-valido");
  document.getElementById("editar-usuario-senha").classList.remove("input-invalido", "input-valido");
  document.getElementById("editar-usuario-confirmar-senha").classList.remove("input-invalido", "input-valido");

}

document.addEventListener("keydown", event => {
  if (event.key === "Escape") {
    fecharModalEditarUsuario();
  }
});

document.getElementById("modal-editar-usuario").addEventListener("click", event => {
  if (event.target.id === "modal-editar-usuario") {
    fecharModalEditarUsuario();
  }
});

async function buscarUsuarioLogado() {

  const response = await fetch("/eu");
  if (!response.ok) {
    throw new Error("Erro ao buscar usuário.");
  }

  return await response.json();
}

async function carregarDadosUsuario() {

  const usuario = await buscarUsuarioLogado();

  estadoEditarUsuario.idUsuario = usuario.id_usuario;
  estadoEditarUsuario.nome = usuario.nome;
  estadoEditarUsuario.credencial = usuario.credencial;
  estadoEditarUsuario.setor = usuario.setor_descricao;
  estadoEditarUsuario.emailOriginal = usuario.email;

  document.getElementById("editar-usuario-nome").textContent = usuario.nome;
  document.getElementById("editar-usuario-info").textContent =
    `Credencial: ${usuario.credencial}; 
     Setor: ${usuario.setor_descricao}`;

  document.getElementById("editar-usuario-email").value = usuario.email;
}

function habilitarEdicaoEmail() {

  estadoEditarUsuario.editandoEmail = true;

  document.getElementById("editar-usuario-email").disabled = false;
  document.getElementById("editar-usuario-email").focus();
}

function habilitarEdicaoSenha() {

  estadoEditarUsuario.editandoSenha = true;

  document.getElementById("editar-usuario-senha").disabled = false;
  document.getElementById("editar-usuario-confirmar-senha").disabled = false;
  document.getElementById("editar-usuario-senha").focus();
}

document.getElementById("editar-usuario-email").addEventListener("input", atualizarEstadoBotao);
document.getElementById("editar-usuario-senha").addEventListener("input", atualizarEstadoBotao);
document.getElementById("editar-usuario-confirmar-senha").addEventListener("input", atualizarEstadoBotao);

async function atualizarUsuarioLogado() {

  const email = document.getElementById("editar-usuario-email").value.trim();
  const senha = document.getElementById("editar-usuario-senha").value;

  const body = {
    email: email === estadoEditarUsuario.emailOriginal ? null : email,
    senha: senha === "" ? null : senha 
  };

  const response = await fetch("/eu", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" }, 
    body: JSON.stringify(body) });

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail || "Erro ao atualizar usuário.");
    return;
  }

  alert("Usuário atualizado com sucesso.");
  fecharModalEditarUsuario();
}
