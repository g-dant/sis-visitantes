let idVisitante = null;
let idVeiculo = null;
let idEmpresa = null;
let timeoutEmpresa = null;

async function buscarVisitantePorCpf() {

  const cpf = (document.getElementById("visitante-cpf").value.trim());
  if (!cpf) {
    return;
  }

  const response = await fetch(`/visitantes/cpf/${cpf}`);
  if (!response.ok) {
    return;
  }

  const visitante = await response.json();

  if (!visitante) {

    idVisitante = null;
    idEmpresa = null;

    limparVisitante();
    desbloquearVisitante();

    const status = document.getElementById("status-visitante");

    status.style.display = "block";
    status.innerText = "Novo visitante";
    status.className = "status-cadastro status-novo";

    return;
  }

  idVisitante = visitante.id;
  idEmpresa = visitante.id_empresa;

  document.getElementById("visitante-nome").value = visitante.nome || "";
  document.getElementById("visitante-email").value = visitante.email || "";
  document.getElementById("visitante-celular").value = visitante.celular || "";
  document.getElementById("empresa-nome").value = visitante.empresa_nome || "";
  document.getElementById("visitante-rg").value = visitante.rg || "";

  const status = document.getElementById("status-visitante");

  status.style.display = "block";
  status.innerText = "Visitante encontrado";
  status.className = "status-cadastro status-encontrado";

  bloquearVisitante();

}

function bloquearVisitante() {

  const campos = [
    "visitante-nome",
    "visitante-email",
    "visitante-celular",
    "visitante-rg",
    "empresa-nome" ];

  for (const id of campos) {

    const campo = document.getElementById(id);

    campo.readOnly = true;
    campo.tabIndex = -1;
    campo.classList.add("campo-readonly");
  }
}

function desbloquearVisitante() {

  const campos = [
    "visitante-nome",
    "visitante-email",
    "visitante-celular",
    "visitante-rg",
    "empresa-nome" ];

  for (const id of campos) {

    const campo = document.getElementById(id);

    campo.readOnly = false;
    campo.tabIndex = 0;
    campo.classList.remove("campo-readonly");
  }
}


async function buscarVeiculoPorPlaca() {

  const placa = (document.getElementById("veiculo-placa").value.trim());
  if (!placa) { return; }

  const response = await fetch(`/veiculos/placa/${placa}`);
  if (!response.ok) {
    return;
  }

  const veiculo = await response.json();
  if (!veiculo) {

    const status = document.getElementById("status-veiculo");

    status.style.display = "block";
    status.innerText = "Novo veículo";
    status.className = "status-cadastro status-novo";

    idVeiculo = null;
    limparVeiculo();
    desbloquearVeiculo();

    return;
  }

  idVeiculo = veiculo.id;

  document.getElementById("veiculo-marca").value = veiculo.marca || "";
  document.getElementById("veiculo-cor").value = veiculo.cor || "";
  document.getElementById("veiculo-tipo").value = veiculo.tipo || "";
  document.getElementById("veiculo-observacoes").value = veiculo.observacoes || "";

  const status = document.getElementById("status-veiculo");

  status.style.display = "block";
  status.innerText = "Veículo encontrado";
  status.className = "status-cadastro status-encontrado";

  bloquearVeiculo();
}

function limparVeiculo() {

  document.getElementById("veiculo-marca").value = "";
  document.getElementById("veiculo-cor").value = "";
  document.getElementById("veiculo-tipo").value = "";
  document.getElementById("veiculo-observacoes").value = "";
}

function bloquearVeiculo() {

  const campos = [
    "veiculo-marca",
    "veiculo-cor",
    "veiculo-tipo",
    "veiculo-observacoes" ];

  for (const id of campos) {

    const campo = document.getElementById(id);

    campo.readOnly = true;
    campo.tabIndex = -1;
    campo.classList.add("campo-readonly");
  }
}

function desbloquearVeiculo() {

  const campos = [
    "veiculo-marca",
    "veiculo-cor",
    "veiculo-tipo",
    "veiculo-observacoes" ];

  for (const id of campos) {

    const campo = document.getElementById(id);

    campo.readOnly = false;
    campo.tabIndex = 0;
    campo.classList.remove("campo-readonly");
  }
}

async function pesquisarEmpresa() {

  const campo = document.getElementById("empresa-nome");
  const nome = campo.value.trim();

  idEmpresa = null;

  if (nome.length < 2) {
    limparSugestoesEmpresa();
    return;
  }

  clearTimeout(timeoutEmpresa);

  timeoutEmpresa = setTimeout(async () => {
    const response = await fetch(`/empresas?nome=${encodeURIComponent(nome)}`);
    if (!response.ok) {
      return;
    }

    const empresas = await response.json();
    renderizarEmpresas(empresas);
  }, 300);
}

function renderizarEmpresas(empresas) {

  const lista = document.getElementById("empresa-sugestoes");
  lista.innerHTML = "";

  for (const empresa of empresas) {

    const item = document.createElement("div");

    item.className = "autocomplete-item";
    item.innerText = empresa.nome;
    item.onclick = () => selecionarEmpresa(empresa);
    lista.appendChild(item);
  }
}

function selecionarEmpresa(empresa) {
  idEmpresa = empresa.id;
  document.getElementById("empresa-nome").value = empresa.nome;
  limparSugestoesEmpresa();
}

function limparSugestoesEmpresa() {
  document.getElementById("empresa-sugestoes").innerHTML = "";
}

async function salvarEdicao() {

  const payload = {

    id_visitante: idVisitante,
    id_empresa: idEmpresa,
    id_status_autorizacao: idStatusAutorizacao,
    id_setor_solicitante: idSetorSolicitante,
    id_veiculo: idVeiculo,

    primeiro_dia: document.getElementById("primeiro-dia").value,
    ultimo_dia: document.getElementById("ultimo-dia").value
  };

  console.log(payload);

  const response =
    await fetch(
      `/autorizacoes/${idAutorizacaoEmEdicao}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload) });

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail || erro.message || "Erro ao atualizar autorização.");
    return;
  }

  alert("Autorização atualizada com sucesso.");
  closeModalVisitantes();
  await carregarAutorizacoes();
}

async function salvarAutorizacao() {

  if (!document.getElementById("visitante-cpf").value) {
    alert("Informe o CPF.");
    return;
  }

  if (!document.getElementById("visitante-nome").value) {
    alert("Informe o nome.");
    return;
  }

  if (idAutorizacaoEmEdicao !== null) {
    return await salvarEdicao();
  }

  const payload = {

    cpf: document.getElementById("visitante-cpf").value,
    rg: document.getElementById("visitante-rg").value,
    nome: document.getElementById("visitante-nome").value,
    email: document.getElementById("visitante-email").value,
    celular: document.getElementById("visitante-celular").value,
    empresa_nome: document.getElementById("empresa-nome").value,
    empresa_cnpj: null,
    placa: document.getElementById("veiculo-placa").value,
    marca: document.getElementById("veiculo-marca").value,
    cor: document.getElementById("veiculo-cor").value,
    tipo: document.getElementById("veiculo-tipo").value,
    observacoes_veiculo: document.getElementById("veiculo-observacoes").value,
    primeiro_dia: document.getElementById("primeiro-dia").value,
    ultimo_dia: document.getElementById("ultimo-dia").value

  };

  let url;
  let metodo;

  if (idAutorizacaoEmEdicao === null) {
    url = "/autorizacoes/emissao";
    metodo = "POST";
  } else {
    url = `/autorizacoes/${idAutorizacaoEmEdicao}`;
    metodo = "PUT";
  }

  const response = await fetch(
    url,
    { method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload) }
  );

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail || erro.message || "Erro ao emitir autorização.");
    return;
  }

  closeModalVisitantes();
  await carregarAutorizacoes();
}

function limparVisitante() {

  document.getElementById("visitante-rg").value = "";
  document.getElementById("visitante-nome").value = "";
  document.getElementById("visitante-email").value = "";
  document.getElementById("visitante-celular").value = "";
  document.getElementById("empresa-nome").value = "";
}

async function alterarStatusAutorizacao(idAutorizacao, idStatus) {

  const confirmar = confirm("Deseja realmente alterar o status?");
  if (!confirmar) {
    return;
  }

  const response =
    await fetch(
      `/autorizacoes/${idAutorizacao}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ id_status_autorizacao: idStatus }) });

  if (!response.ok) {
    const erro = await response.json();
    alert(erro.detail || erro.message || "Erro ao alterar status.");
    return;
  }

  await carregarAutorizacoes();
}
