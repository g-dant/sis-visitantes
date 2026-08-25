function formatarData(dataIso) {

  if (!dataIso) {
    return "";
  }

  const [ano, mes, dia] = dataIso.substring(0, 10).split("-");

  return `${dia}/${mes}/${ano}`;
}

function desformatarData(dataBr) {

  if (!dataBr) {
    return "";
  }

  const [dia, mes, ano] = dataBr.split("/");
  return `${ano}-${mes}-${dia}`;
}

function emailValido(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function senhaForte(senha) {

  return (
    senha.length >= 8

    && /[a-z]/.test(senha)
    && /[A-Z]/.test(senha)
    && /[0-9]/.test(senha)
    && /[^A-Za-z0-9]/.test(senha)
  );
}

function marcarCampoValido(campo) {

  if (typeof campo === "string") {
    campo = document.getElementById(campo);
  }

  if (!campo) {
    return;
  }

  campo.classList.remove("campo-invalido", "input-invalido");
  campo.classList.add("campo-valido", "input-valido");
}


function marcarCampoInvalido(campo, campoErro = null, mensagem = "") {

  if (typeof campo === "string") {
    campo = document.getElementById(campo);
  }

  if (typeof campoErro === "string") {
    campoErro = document.getElementById(campoErro);
  }

  if (!campo) {
    return;
  }

  campo.classList.remove("campo-valido", "input-valido");
  campo.classList.add("campo-invalido", "input-invalido");

  if (campoErro) {
    campoErro.textContent = mensagem;
  }
}


function limparValidacaoCampo(campo, campoErro = null) {

  if (typeof campo === "string") {
    campo = document.getElementById(campo);
  }

  if (typeof campoErro === "string") {
    campoErro = document.getElementById(campoErro);
  }

  if (!campo) {
    return;
  }

  campo.classList.remove(
    "campo-invalido",
    "campo-valido",
    "input-invalido",
    "input-valido"
  );

  if (campoErro) {
    campoErro.textContent = "";
  }
}

function formatarCpf(cpfSoNumeros) {

  if (cpfSoNumeros.length !== 11) {
    return 'CPF inválido';
  }

  return (cpfSoNumeros.substring(0, 3) + '.' +
	  cpfSoNumeros.substring(3, 6) + '.' +
	  cpfSoNumeros.substring(6, 9) + '-' +
	  cpfSoNumeros.substring(9, 11));
}

function escapeChars(strIn) {

  return strIn
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
