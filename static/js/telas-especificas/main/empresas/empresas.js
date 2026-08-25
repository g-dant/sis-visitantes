let empresasCadastro = [];
let empresaEmEdicao = null;

async function carregarEmpresasCadastro() {

  try {

    const response = await fetch("/empresas", 
      { headers: { Authorization: `Bearer ${obterToken()}` }});

    if (!response.ok) {
      throw new Error("Erro ao carregar empresas.");
    }

    empresasCadastro = await response.json();
    renderizarCadastroEmpresas();

  } catch (erro) {
    console.error("Erro ao carregar empresas:", erro);
    alert("Erro ao carregar empresas");
  }
}

function obterEmpresasFiltradas() {

  const texto =
    document
      .getElementById("filtro-empresas")
      .value
      .trim()
      .toLowerCase();

  const ativo =
    document
      .getElementById("filtro-empresas-ativo")
      .value;

  return empresasCadastro.filter(
    empresa => {

      const correspondeTexto =
        !texto ||
        (empresa.nome || "")
          .toLowerCase()
          .includes(texto) ||
        (empresa.cnpj || "")
          .toLowerCase()
          .includes(texto);
  
      const correspondeAtivo =
        ativo === "" ||
        String(empresa.ativo) === ativo;

      return (
        correspondeTexto &&
        correspondeAtivo
      );
    }
  );
}

function renderizarCadastroEmpresas() {

  const tbody = document.getElementById("empresas-tbody");

  if (!tbody) {
    return;
  }

  tbody.innerHTML = "";

  const empresasFiltradas = obterEmpresasFiltradas();

  for (const empresa of empresasFiltradas) {

    const tr = document.createElement("tr");

    const btnAdicionarEmpresa = `
      <button class="btn btn-primary" title="Editar empresa" 
        onclick="abrirModalNovaEmpresa('Editar empresa', 
	  {
            id: ${empresa.id}, 
	    nome: ${escapeChars(JSON.stringify(empresa.nome))},
	    cnpj: ${escapeChars(JSON.stringify(empresa.cnpj))},
	    ativo: ${empresa.ativo}
	  })">
        <i class="fa-solid fa-pen"></i>
      </button>`
		
    const btnExcluirEmpresa = `
      <button class="btn btn-danger" title="Remover empresa" 
        onclick="removerEmpresa(${empresa.id})">
        <i class="fa-solid fa-trash"></i>
      </button>`

    tr.innerHTML = `
      <td>${empresa.nome ?? ""}</td>
      <td style="text-align: center;">${empresa.cnpj ?? ""}</td>
      <td style="text-align: center;">${empresa.ativo ? "Sim" : "Não"}</td>

      <td style="text-align: center;">
        ${btnAdicionarEmpresa} 
	${empresa.pode_excluir ? btnExcluirEmpresa : ""}
      </td>`;

    tbody.appendChild(tr);
  }
}

async function abrirModalCadastroEmpresas() {

  const modal = document.getElementById("modalCadastroEmpresas");
  modal.style.display = "flex";

  const filtro = document.getElementById("filtro-empresas");
  const filtroAtivo = document.getElementById("filtro-empresas-ativo");

  filtro.oninput = renderizarCadastroEmpresas;
  filtroAtivo.onchange = renderizarCadastroEmpresas;

  await carregarEmpresasCadastro();
}

function fecharModalCadastroEmpresas() {

  const modal = document.getElementById("modalCadastroEmpresas");
  modal.style.display = "none";
}

function fecharModalNovaEmpresa() {

  const modal = document.getElementById("modalNovaEmpresa");
  modal.style.display = "none";
  empresaEmEdicao = null;
}

async function abrirModalNovaEmpresa(titulo = "Nova empresa", dados = {}) {

  limparModalNovaEmpresa();
  empresaEmEdicao = dados.id ?? null;

  document.getElementById("modal-nova-empresa-titulo").textContent = titulo;

  document.getElementById("nova-empresa-nome").value = dados.nome ?? "";
  document.getElementById("nova-empresa-cnpj").value = dados.cnpj ?? "";

  document.getElementById("nova-empresa-ativo").checked = dados.ativo ?? true;

  const modal = document.getElementById("modalNovaEmpresa");
  modal.style.display = "flex";

}

function limparModalNovaEmpresa() {

  document.getElementById("nova-empresa-nome").value = "";
  document.getElementById("nova-empresa-cnpj").value = "";
  document.getElementById("nova-empresa-ativo").checked = true;
  document.querySelectorAll("#modalNovaEmpresa .input-invalido").forEach(
    campo => campo.classList.remove("input-invalido"));
}

function validarNovaEmpresa() {

  const nome = document.getElementById("nova-empresa-nome").value.trim();
  const campoNome = document.getElementById("nova-empresa-nome");

  campoNome.classList.remove("input-invalido");

  let valido = true;

  if (!nome) {
    campoNome.classList.add("input-invalido");
    valido = false;
  }

  return valido;
}

async function salvarNovaEmpresa() {

  if (!validarNovaEmpresa()) {
    return;
  }

  const payload = {
    nome: document.getElementById("nova-empresa-nome").value.trim(),
    cnpj: document.getElementById("nova-empresa-cnpj").value.trim(),
    ativo: document.getElementById("nova-empresa-ativo").checked
  };

  try {

    const url =
      empresaEmEdicao === null
        ? "/empresas"
        : `/empresas/${empresaEmEdicao}`;

    const method =
      empresaEmEdicao === null
        ? "POST"
        : "PUT";

    const response = await fetch(url, 
      {
        method: method, 
	headers: 
          { 
            "Content-Type": "application/json",
            Authorization: `Bearer ${obterToken()}`
          }, 
        body: JSON.stringify(payload)
      });

    if (!response.ok) {

      const erro = await response.json();
      alert(erro.detail || erro.message || "Erro ao salvar empresa.");

      return;
    }

    alert(empresaEmEdicao === null ? 
      "Empresa adicionada com sucesso" : 
      "Empresa atualizada com sucesso");

    fecharModalNovaEmpresa();
    empresaEmEdicao = null;

    await carregarEmpresasCadastro();

  } catch (erro) {
    console.error("Erro ao salvar empresa:", erro);
    alert("Erro ao salvar empresa.");
  }

}

async function removerEmpresa(idEmpresa) {

  const confirmar = confirm("Deseja realmente remover esta empresa?");
  if (!confirmar) {
    return;
  }

  try {
    const response = await fetch(`/empresas/${idEmpresa}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${obterToken()}` }
    });

    if (!response.ok) {
      const erro = await response.json();
      alert(erro.detail || erro.message || "Erro ao remover empresa.");

      return;			          
    }

    alert("Empresa removida com sucesso");
    await carregarEmpresasCadastro();

  } catch (erro) {
    console.error("Erro ao remover empresa:", erro);
    alert("Erro ao remover empresa.");
  }
}
