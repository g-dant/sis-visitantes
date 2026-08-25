const cores_status = {
    'Autorizada': 'active',
    'Pendente': 'pending',
    'Revogada': 'revoked',
    'Expirada': 'expired'
};

inicializar();

async function inicializar() {

  await exigirPermissao("ROTA_MAIN");

  carregarUsuarioCabecalho();
  await carregarStatus();
  await carregarSetores();
  await carregarPainel();
  await iniciarAtualizacaoAutomatica();
  await carregarAutorizacoes();

  inicializarModalAutorizacao();

  document.getElementById("btn-salvar-autorizacao").addEventListener("click", salvarAutorizacao);
  document.getElementById("qtd-registros").addEventListener("change", alterarQuantidadeRegistros);
}

function toggleCardMenu(idAutorizacao) {
  const menu = document.getElementById(`menu-${idAutorizacao}`);
  if (!menu) { return; }
  menu.classList.toggle("show");
}

window.addEventListener(
  "click", function(event) {

    if (!event.target.closest(".mobile-card-menu")) {
      document.querySelectorAll(".card-dropdown").forEach(menu =>
        menu.classList.remove("show"));
    }
  }
);

async function carregarAutorizacoes() {

  const response = await fetch("/autorizacoes");
  if (!response.ok) {
    console.error("Erro ao carregar autorizações");
    return;
  }

  autorizacoes = await response.json();
  renderizarAutorizacoes();
}

async function renderizarAutorizacoes() {

  let botaoVisualizar = "";
  let botaoEditar = "";
  let botaoStatus = "";

  let botaoVisualizarMobile = "";
  let botaoEditarMobile = "";
  let botaoStatusMobile = "";

  const tbody = document.getElementById("autorizacoes-tbody");
  const mobileCards = document.getElementById("autorizacoes-cards");

  tbody.innerHTML = "";
  mobileCards.innerHTML = "";

  for (const autorizacao of obterItensPaginaAtual(obterItensFiltrados())) {

    botaoVisualizar = 
     `<button class="icon view" onclick="visualizarAutorizacao(${autorizacao.id})">
        <i class="fa-solid fa-eye"></i>
      </button>`;

    botaoEditar =
      `<button class="icon edit" onclick="editarAutorizacao(${autorizacao.id})">
         <i class="fa-solid fa-pen"></i>
       </button>`

    botaoVisualizarMobile =
      `<button onclick="visualizarAutorizacao(${autorizacao.id})">
         Visualizar
       </button>`

    botaoEditarMobile = 
      `<button onclick=" editarAutorizacao(${autorizacao.id})">
         Editar
       </button>`

    if (autorizacao.status_nome === "Revogada") {

      botaoStatus = `
        <button class="icon undo" onclick="alterarStatusAutorizacao(${autorizacao.id}, 1)">
          <i class="fa-solid fa-rotate-left"></i>
        </button>`;

      botaoStatusMobile = `<button onclick="alterarStatusAutorizacao(
        ${autorizacao.id}, ${autorizacao.id_status_autorizacao_anterior})">
        Restaurar</button>`;

    } else {
      botaoStatus = `
        <button class="icon delete"onclick="alterarStatusAutorizacao(${autorizacao.id}, 3)">
          <i class="fa-solid fa-xmark"></i>
        </button>
      `;

      botaoStatusMobile = `<button onclick="alterarStatusAutorizacao(${autorizacao.id}, 3)">
        Revogar</button>`;
    }

    tbody.innerHTML += `
      <tr>

        <td style="text-align: center;">
          <span class="badge ${cores_status[autorizacao.status_exibicao]}">
            ${autorizacao.status_exibicao}
          </span>
        </td>

        <td>${autorizacao.visitante_nome.toUpperCase()}</td>

	<td style="text-align: center;">${formatarCpf(autorizacao.cpf)}</td>

        <td style="text-align: center;">${formatarData(autorizacao.primeiro_dia)}</td>

        <td style="text-align: center;">${formatarData(autorizacao.ultimo_dia)}</td>

        <td style="text-align: center;">
	  <span title='${'Solicitação de ' + autorizacao.solicitante_nome}'
	    style="color: #007bff; text-decoration: underline; cursor: help;">
            ${autorizacao.setor_solicitante_codigo}
	  </span>
        </td>

	<td style="text-align: center;">
	  ${autorizacao.empresa_nome}
	</td>

        <td>
          <div class="actions">
            ${ possuiPermissao("AUTORIZACAO_VISUALIZAR") ?  botaoVisualizar : "" }
	    ${ possuiPermissao("AUTORIZACAO_EDITAR") ? botaoEditar : "" }
            ${ possuiPermissao("AUTORIZACAO_ALTERAR_STATUS") ? botaoStatus : "" } 
          </div>
        </td>

      </tr>`;

    mobileCards.innerHTML += `
    <div class="mobile-card">
      <div class="mobile-card-menu">

        <button class="btn menu-btn" onclick="toggleCardMenu(${autorizacao.id})">
        ⋮
        </button>

        <div id="menu-${autorizacao.id}" class="card-dropdown">
            ${ possuiPermissao("AUTORIZACAO_VISUALIZAR") ?  botaoVisualizarMobile : "" }
            ${ possuiPermissao("AUTORIZACAO_EDITAR") ? botaoEditarMobile : "" }
            ${ possuiPermissao("AUTORIZACAO_ALTERAR_STATUS") ? botaoStatusMobile : "" }
        </div>
      </div>

      <h3>${autorizacao.visitante_nome.toUpperCase()}</h3>

      <p>
        <span class="badge ${cores_status[autorizacao.status_exibicao]}">
          ${autorizacao.status_exibicao}
        </span>
      </p>
  
      <p>De: ${formatarData(autorizacao.primeiro_dia)}</p>
      <p>Até: ${formatarData(autorizacao.ultimo_dia)}</p>
      <p>
        Solicitante:
        ${autorizacao.setor_solicitante_codigo}
        -
        ${autorizacao.solicitante_nome}
      </p>
    </div>`;
  }
 
  renderizarPaginacao();
}

