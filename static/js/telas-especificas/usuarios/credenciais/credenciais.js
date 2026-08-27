let credenciais = [];
let paginaAtualCredenciais = 1;
let permissoesCredencial = [];
let credencialEmEdicao = null;

document.addEventListener(
  "DOMContentLoaded",
  () => {

    const filtro = document.getElementById("filtro-credenciais");
    const filtroAtivo = document.getElementById("filtro-credenciais-ativo");

    filtro.addEventListener("input", () => {
      paginaAtualCredenciais = 1;
      renderizarCadastroCredenciais();
    });

    filtroAtivo.addEventListener("change", () => {
      paginaAtualCredenciais = 1;
      renderizarCadastroCredenciais();
    });
  }
);

document.getElementById("credenciais-qtd-registros").addEventListener(
  "change", () => {
    paginaAtualCredenciais = 1;
    renderizarCadastroCredenciais();
  }
);

async function carregarCredenciais() {

  try {

    const response = await fetch("/credenciais", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${obterToken()}`
      }});

    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail || "Erro ao carregar credenciais.");
    }

    credenciais = await response.json();
    renderizarCadastroCredenciais();

  } catch (erro) {

    console.error("Erro ao carregar credenciais:", erro);
    alert(erro.message || "Erro ao carregar credenciais.");
  }
}


function renderizarCadastroCredenciais() {

  const tbody = document.getElementById("credenciais-tbody");
  tbody.innerHTML = "";

  const credenciaisPaginaAtual = obterCredenciaisPaginaAtual();

  for (const credencial of credenciaisPaginaAtual) {

    const tr = document.createElement("tr");

    const btnEditarCredencial = `
      <button
        class="icon edit"
        title="Editar credencial"
        onclick="abrirModalNovaCredencial(
          'Editar credencial',
          {
            id: ${credencial.id},
            nome: ${escapeChars(JSON.stringify(credencial.nome))},
            descricao: ${escapeChars(JSON.stringify(credencial.descricao))},
            ativo: ${credencial.ativo}
          }
        )">
        <i class="fa-solid fa-pen"></i>
      </button>`;

    const btnExcluirCredencial = `
      <button
        class="icon delete"
        type="button"
        title="Excluir credencial"
        onclick="removerCredencial(${credencial.id})">
        <i class="fa-solid fa-trash"></i>
      </button>`;

    tr.innerHTML = `
      <td>${credencial.nome ?? ""}</td>

      <td>${credencial.descricao ?? ""}</td>

      <td style="text-align: center;">
        ${credencial.ativo ? "Sim" : "Não"}
      </td>

      <td style="text-align: center;">
        ${btnEditarCredencial}
	${credencial.pode_excluir ? btnExcluirCredencial : ""}
      </td>`;

    tbody.appendChild(tr);
  }

  renderizarPaginacaoCredenciais();
}


function abrirModalCadastroCredenciais() {
  const modal = document.getElementById("modalCadastroCredenciais");
  modal.style.display = "flex";
  carregarCredenciais();
}


function fecharModalCadastroCredenciais() {
  const modal = document.getElementById("modalCadastroCredenciais");
  modal.style.display = "none";
}

function obterCredenciaisFiltradas() {

  const texto = document.getElementById("filtro-credenciais")
    .value.trim().toLowerCase();

  const ativo = document.getElementById("filtro-credenciais-ativo")
    .value;

  return credenciais.filter(
    credencial => {

      const correspondeTexto =
        !texto ||
        (credencial.nome || "")
          .toLowerCase()
          .includes(texto) ||
        (credencial.descricao || "")
          .toLowerCase()
          .includes(texto);

      const correspondeAtivo =
        ativo === "" ||
        String(credencial.ativo) === ativo;

      return (correspondeTexto && correspondeAtivo);
    }
  );
}

function obterCredenciaisPaginaAtual() {

  const credenciaisFiltradas = obterCredenciaisFiltradas();

  const quantidade = Number(document.getElementById("credenciais-qtd-registros").value);

  if (quantidade === -1) {
    return credenciaisFiltradas;
  }

  const inicio = (paginaAtualCredenciais - 1) * quantidade;
  const fim = inicio + quantidade;

  return credenciaisFiltradas.slice(inicio, fim);
}

function renderizarPaginacaoCredenciais() {

  const credenciaisFiltradas = obterCredenciaisFiltradas();

  const quantidade = Number(document.getElementById("credenciais-qtd-registros").value);

  const totalPaginas = (quantidade === -1) ? 
    1 : Math.ceil(credenciaisFiltradas.length / quantidade);

  const container = document.getElementById("credenciais-pagination");

  container.innerHTML = "";

  for (let pagina = 1; pagina <= totalPaginas; pagina++) {

    const botao = document.createElement("button");

    botao.textContent = pagina;
    botao.classList.add("btn");

    if (pagina === paginaAtualCredenciais) {
      botao.classList.add("btn-primary");
    }

    botao.addEventListener("click", () => {
      paginaAtualCredenciais = pagina;
      renderizarCadastroCredenciais();
    });

    container.appendChild(botao);
  }
}

async function abrirModalNovaCredencial(titulo = "Nova credencial", credencial = null) {

  credencialEmEdicao = credencial;

  document.getElementById("titulo-modal-credencial").textContent = titulo;
  limparModalNovaCredencial();

  if (credencial) {

    document.getElementById("nova-credencial-nome").value = credencial.nome ?? "";
    document.getElementById("nova-credencial-descricao").value = credencial.descricao ?? "";
  }

  const modal = document.getElementById("modalNovaCredencial");

  modal.style.display = "flex"
  await carregarPermissoesCredencial();
}

function fecharModalNovaCredencial() {

  const modal = document.getElementById("modalNovaCredencial");
  modal.style.display = "none"
  credencialEmEdicao = null;
}

function limparModalNovaCredencial() {

  document.getElementById("nova-credencial-nome").value = "";
  document.getElementById("nova-credencial-descricao").value = "";
  document.getElementById("erro-nova-credencial-nome").textContent = "";
  document.getElementById("nova-credencial-nome").classList.remove("input-invalido");
  document.getElementById("nova-credencial-permissoes-tbody").innerHTML = "";

  permissoesCredencial = [];
}

async function carregarPermissoesCredencial() {

  try {

    let url;

    if (credencialEmEdicao) {
      url = `/credenciais/${credencialEmEdicao.id}/permissoes`;
    } else {
      url = "/permissoes";
    }

    const response =
      await fetch(
        url,
        {
          method: "GET",
          headers: {
            Authorization:
              `Bearer ${obterToken()}`
          }
        }
      );

    if (!response.ok) {

      const erro = await response.json();
      throw erro;
    }

    const permissoes = await response.json();

    permissoesCredencial = permissoes;

    renderizarPermissoesCredencial(permissoesCredencial);

  } catch (erro) {

    console.error("Erro ao carregar permissões:", erro);
    alert("Erro ao carregar permissões.");
  }
}

function renderizarPermissoesCredencial(permissoes) {

  const tbody = document.getElementById("nova-credencial-permissoes-tbody");
  tbody.innerHTML = "";

  for (const permissao of permissoes) {

    const habilitado = Boolean(permissao.habilitado);
    const tr = document.createElement("tr");

    const btnAcao = habilitado ? `
          <button
            class="icon delete"
            type="button"
            title="Desabilitar permissão"
	    onclick="alterarPermissaoCredencial(${permissao.id})">
          <i class="fa-solid fa-ban"></i>
          </button>
        `
        : `
          <button
            class="icon edit"
            type="button"
            title="Habilitar permissão"
	    onclick="alterarPermissaoCredencial(${permissao.id})">
            <i class="fa-solid fa-check"></i>
          </button>
        `;

    tr.innerHTML = `
      <td>${permissao.codigo ?? ""}</td>
      
      <td>${permissao.descricao ?? ""}</td>

      <td style="text-align: center;">
        ${habilitado ? "Sim" : "Não"}
      </td>

      <td style="text-align: center;">
        ${btnAcao}
      </td>`;

    tbody.appendChild(tr);
  }
}

async function alterarPermissaoCredencial(idPermissao) {

  const permissao = permissoesCredencial.find(
    permissao => permissao.id === idPermissao);

  if (!permissao) {
    return;
  }

  if (!credencialEmEdicao) {

    permissao.habilitado = !permissao.habilitado;
    renderizarPermissoesCredencial(permissoesCredencial);

    return;
  }

  await alterarPermissaoCredencialEdicao(permissao);
}

async function salvarNovaCredencial() {

  if (!validarNovaCredencial()) {
    return;
  }

  const nome =
    document
      .getElementById("nova-credencial-nome")
      .value
      .trim();

  const descricao =
    document
      .getElementById("nova-credencial-descricao")
      .value
      .trim();

  try {

    let response;

    if (credencialEmEdicao) {

      response = await fetch(
        `/credenciais/${credencialEmEdicao.id}`,
        {
          method: "PUT",

          headers: {
            "Content-Type": "application/json",
            Authorization:
              `Bearer ${obterToken()}`
          },

          body: JSON.stringify({
            nome,
            descricao: descricao || null,
            ativo: credencialEmEdicao.ativo
          })
        }
      );

    } else {

      const idsPermissoes =
        permissoesCredencial
          .filter(permissao => permissao.habilitado)
          .map(permissao => permissao.id);

      response = await fetch(
        "/credenciais",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization:
              `Bearer ${obterToken()}`
          },

          body: JSON.stringify({
            nome,
            descricao: descricao || null,
            ativo: true,
            ids_permissoes: idsPermissoes
          })
        }
      );
    }

    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail || "Erro ao salvar credencial.");
    }

    fecharModalNovaCredencial();
    await carregarCredenciais();

  } catch (erro) {

    console.error("Erro ao salvar credencial:", erro);
    alert(erro.message || "Erro ao salvar credencial.");
  }
}

async function alterarPermissaoCredencialEdicao(permissao) {

  const habilitar = !permissao.habilitado;
  const metodo = habilitar ? "POST" : "DELETE";

  try {

    const response = await fetch(
      `/credenciais/${credencialEmEdicao.id}/permissoes/${permissao.id}`,
      {
        method: metodo,
        headers: {
          Authorization: `Bearer ${obterToken()}`
        }
      }
    );

    if (!response.ok) {

      const erro = await response.json();
      throw new Error(erro.detail || "Erro ao alterar permissão.");
    }

    /*
     * Só alteramos o estado visual depois
     * que o backend confirmou a operação.
     */
    permissao.habilitado = habilitar;
    renderizarPermissoesCredencial(permissoesCredencial);

  } catch (erro) {

    console.error("Erro ao alterar permissão:", erro);
    alert(erro.message || "Erro ao alterar permissão.");
  }
}

function validarNovaCredencial() {

  const campoNome = document.getElementById("nova-credencial-nome");
  const erroNome = document.getElementById("erro-nova-credencial-nome");

  const nome = campoNome.value.trim();

  if (!nome) {

    erroNome.textContent = "O nome da credencial é obrigatório.";
    campoNome.classList.add("input-invalido");
    campoNome.focus();

    return false;
  }

  erroNome.textContent = "";
  campoNome.classList.remove("input-invalido");

  return true;
}

async function removerCredencial(idCredencial) {

  const credencial = credenciais.find(
    credencial => credencial.id === idCredencial);

  if (!credencial) {
    return;
  }

  const confirmar = confirm(`Deseja realmente excluir a credencial "${credencial.nome}"?`);

  if (!confirmar) {
    return;
  }

  try {

    const response = await fetch(
      `/credenciais/${idCredencial}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${obterToken()}`
        }
      }
    );

    if (!response.ok) {

      const erro = await response.json();

      throw new Error(
        erro.detail ||
        "Erro ao excluir credencial."
      );
    }

    credenciais = credenciais.filter(
      credencial => credencial.id !== idCredencial);

    renderizarCadastroCredenciais();
    alert("Credencial excluída com sucesso.");

  } catch (erro) {

    console.error("Erro ao excluir credencial:", erro);
    alert(erro.message || "Erro ao excluir credencial.");
  }
}
