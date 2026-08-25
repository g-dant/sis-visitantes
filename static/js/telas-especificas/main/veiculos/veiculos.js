let veiculosCadastro = [];

let paginaAtualVeiculos = 1;
let registrosPorPaginaVeiculos = 10;

let veiculosEmEdicao = null;

document.addEventListener(
  "DOMContentLoaded",
  () => {
    document
      .getElementById("filtro-veiculos")
      .addEventListener("input", () => {
        paginaAtualVeiculos = 1;
	renderizarCadastroVeiculos();
      });

    document
      .getElementById("filtro-veiculos-ativo")
      .addEventListener("change", () => {
        paginaAtualVeiculos = 1;
	renderizarCadastroVeiculos();
      });

    document
      .getElementById("veiculos-qtd-registros")
      .addEventListener("change", () => {
        registrosPorPaginaVeiculos = parseInt(
          document.getElementById("veiculos-qtd-registros").value);

      paginaAtualVeiculos = 1;
      renderizarCadastroVeiculos();
    });
  }
);

async function carregarVeiculosCadastro() {

  try {

    const response = await fetch(
        "/veiculos",
        {
          headers: {
            Authorization: `Bearer ${obterToken()}`
          }
        }
      );

    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail || "Erro ao carregar veículos.");
    }

    veiculosCadastro = await response.json();
    renderizarCadastroVeiculos();

  } catch (erro) {
    console.error("Erro ao carregar veículos:", erro);
    alert("Erro ao carregar veículos.");
  }
}

function obterVeiculosFiltrados() {

  const texto =
    document
      .getElementById("filtro-veiculos")
      .value
      .trim()
      .toLowerCase();

  const ativo =
    document
      .getElementById("filtro-veiculos-ativo")
      .value;

  return veiculosCadastro.filter(
    veiculo => {

      const correspondeTexto =
        !texto ||

        (veiculo.placa || "")
          .toLowerCase()
          .includes(texto) ||

        (veiculo.marca || "")
          .toLowerCase()
          .includes(texto) ||

        (veiculo.cor || "")
          .toLowerCase()
          .includes(texto) ||

        (veiculo.tipo || "")
          .toLowerCase()
          .includes(texto);

      const correspondeAtivo =
        ativo === "" ||
        String(veiculo.ativo) === ativo;

      return (
        correspondeTexto &&
        correspondeAtivo
      );
    }
  );
}

function obterVeiculosPaginaAtual() {

  const veiculosFiltrados = obterVeiculosFiltrados();

  if (registrosPorPaginaVeiculos === -1) {
    return veiculosFiltrados;
  }

  const inicio = (paginaAtualVeiculos - 1) * registrosPorPaginaVeiculos;
  const fim = inicio + registrosPorPaginaVeiculos;

  return veiculosFiltrados.slice(inicio, fim);
}

function renderizarCadastroVeiculos() {

  const tbody = document.getElementById("veiculos-tbody");

  tbody.innerHTML = "";

  const veiculosCadastroPaginaAtual = obterVeiculosPaginaAtual();
  for (const veiculo of veiculosCadastroPaginaAtual) {

    const tr = document.createElement("tr");

    const btnEditarVeiculo = `
      <button
        class="btn btn-primary"
        title="Editar veículo"
        onclick="abrirModalNovoVeiculo(
          'Editar veículo',
          {
            id: ${veiculo.id},
            placa: ${escapeChars(JSON.stringify(veiculo.placa))},
            marca: ${escapeChars(JSON.stringify(veiculo.marca))},
            cor: ${escapeChars(JSON.stringify(veiculo.cor))},
            tipo: ${escapeChars(JSON.stringify(veiculo.tipo))},
            observacoes: ${escapeChars(JSON.stringify(veiculo.observacoes))},
            ativo: ${veiculo.ativo}
          }
        )">
        <i class="fa-solid fa-pen"></i>
      </button>`;

    const btnExcluirVeiculo = `
      <button
        class="btn btn-danger"
        title="Remover veículo"
        onclick="removerVeiculo(${veiculo.id})">
        <i class="fa-solid fa-trash"></i>
      </button>`;

    tr.innerHTML = `
      <td style="text-align: center;">
        ${veiculo.placa ?? ""}
      </td>

      <td>${veiculo.marca ?? ""}</td>

      <td>${veiculo.cor ?? ""}</td>

      <td>${veiculo.tipo ?? ""}</td>

      <td style="text-align: center;">
        ${veiculo.ativo ? "Sim" : "Não"}
      </td>

      <td style="text-align: center;">
        ${btnEditarVeiculo}
        ${veiculo.pode_excluir ? btnExcluirVeiculo : ""}
      </td>
    `;

    tbody.appendChild(tr);
  }

  renderizarPaginacaoVeiculos();
}

function renderizarPaginacaoVeiculos() {

  const container = document.getElementById("veiculos-pagination");
  container.innerHTML = "";

  if (registrosPorPaginaVeiculos === -1) {
    return;
  }

  const totalVeiculos = obterVeiculosFiltrados().length;
  const totalPaginas = Math.ceil(totalVeiculos / registrosPorPaginaVeiculos);

  if (totalPaginas <= 1) {
    return;
  }

  const anterior = document.createElement("button");

  anterior.textContent = "«";
  anterior.disabled = (paginaAtualVeiculos === 1);
  anterior.onclick = () => {

    if (paginaAtualVeiculos > 1) {

      paginaAtualVeiculos--;
      renderizarCadastroVeiculos();
      renderizarPaginacaoVeiculos();
    }
  };

  container.appendChild(anterior);

  for (let i = 1; i <= totalPaginas; i++) {

    const btn = document.createElement("button");
    btn.textContent = i;

    if (i === paginaAtualVeiculos) {
      btn.classList.add("active");
    }

    btn.onclick = () => {
      paginaAtualVeiculos = i;
      renderizarCadastroVeiculos();
      renderizarPaginacaoVeiculos();
    };

    container.appendChild(btn);
  }

  const proxima = document.createElement("button");

  proxima.textContent = "»";
  proxima.disabled = (paginaAtualVeiculos === totalPaginas);
  proxima.onclick = () => {

    if (paginaAtualVeiculos < totalPaginas) {

      paginaAtualVeiculos++;
      renderizarCadastroVeiculos();
      renderizarPaginacaoVeiculos();
    }
  };

  container.appendChild(proxima);
}

async function abrirModalCadastroVeiculos() {
  const modal = document.getElementById("modalCadastroVeiculos");
  modal.style.display = "flex";
  await carregarVeiculosCadastro();
}

function fecharModalCadastroVeiculos() {
  const modal = document.getElementById("modalCadastroVeiculos");
  modal.style.display = "none";
}

function limparModalNovoVeiculo() {

  const campos = [
    "novo-veiculo-placa",
    "novo-veiculo-marca",
    "novo-veiculo-cor",
    "novo-veiculo-tipo",
    "novo-veiculo-observacoes"
  ];

  for (const idCampo of campos) {

    document.getElementById(idCampo).value = "";
  }

  document.getElementById("novo-veiculo-ativo").checked = true;
  document.querySelectorAll("#modalNovoVeiculo .input-invalido")
    .forEach(campo => campo.classList.remove("input-invalido"));

  veiculoEmEdicao = null;
}

function abrirModalNovoVeiculo(titulo = "Novo veículo", dados = null) {

  const modal = document.getElementById("modalNovoVeiculo");
  const tituloModal = document.getElementById("modal-novo-veiculo-titulo");

  limparModalNovoVeiculo();
  tituloModal.textContent = titulo;

  if (dados) {

    veiculoEmEdicao = dados;

    document.getElementById("novo-veiculo-placa").value = dados.placa ?? "";
    document.getElementById("novo-veiculo-marca").value = dados.marca ?? "";
    document.getElementById("novo-veiculo-cor").value = dados.cor ?? "";
    document.getElementById("novo-veiculo-tipo").value = dados.tipo ?? "";
    document.getElementById("novo-veiculo-observacoes").value = dados.observacoes ?? "";
    document.getElementById("novo-veiculo-ativo").checked = Boolean(dados.ativo);
  }

  modal.style.display = "flex";
}

function fecharModalNovoVeiculo() {
  const modal = document.getElementById("modalNovoVeiculo");
  modal.style.display = "none";
}

function validarNovoVeiculo() {

  const campoPlaca = document.getElementById("novo-veiculo-placa");
  const placa = campoPlaca.value.trim();

  campoPlaca.classList.remove("input-invalido");

  let valido = true;

  if (!placa) {
    campoPlaca.classList.add("input-invalido");
    valido = false;
  }

  return valido;
}

async function salvarNovoVeiculo() {

  if (!validarNovoVeiculo()) {
    return;
  }

  const dados = {
    placa:
      document
        .getElementById("novo-veiculo-placa")
        .value
        .trim(),

    marca:
      document
        .getElementById("novo-veiculo-marca")
        .value
        .trim() || null,

    cor:
      document
        .getElementById("novo-veiculo-cor")
        .value
        .trim() || null,

    tipo:
      document
        .getElementById("novo-veiculo-tipo")
        .value
        .trim() || null,

    observacoes:
      document
        .getElementById("novo-veiculo-observacoes")
        .value
        .trim() || null,

    ativo:
      document
        .getElementById("novo-veiculo-ativo")
        .checked
  };

  try {

    const response =
      await fetch(
        "/veiculos",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",

            Authorization:
              `Bearer ${obterToken()}`
          },

          body:
            JSON.stringify(dados)
        }
      );

    if (!response.ok) {

      const erro = await response.json();
      console.error("Erro ao adicionar veículo:", erro);
      alert(erro.detail || erro.message || "Erro ao adicionar veículo.");

      return;
    }

    alert("Veículo adicionado com sucesso");
    fecharModalNovoVeiculo();

    await carregarVeiculosCadastro();

  } catch (erro) {
    console.error("Erro ao adicionar veículo:", erro);
    alert("Erro ao adicionar veículo.");
  }
}

async function removerVeiculo(idVeiculo) {

  const confirmar =
    confirm(
      "Deseja realmente remover este veículo?"
    );

  if (!confirmar) {
    return;
  }

  try {

    const response =
      await fetch(
        `/veiculos/${idVeiculo}`,
        {
          method: "DELETE",
          headers: {
            Authorization:
              `Bearer ${obterToken()}`
          }
        }
      );

    if (!response.ok) {

      const erro =
        await response.json();

      alert(
        erro.detail ||
        erro.message ||
        "Erro ao remover veículo."
      );

      return;
    }

    alert(
      "Veículo removido com sucesso"
    );

    await carregarVeiculosCadastro();

  } catch (erro) {

    console.error(
      "Erro ao remover veículo:",
      erro
    );

    alert(
      "Erro ao remover veículo."
    );
  }
}
