let resultadoImportacao = null;

function arquivoImportacaoSelecionado(event) {

  const arquivo = event.target.files[0];
  const nomeArquivo = document.getElementById("nome-arquivo-importacao");
  const botaoImportar = document.getElementById("btn-importar-autorizacoes");

  if (!arquivo) {
    nomeArquivo.textContent = "Nenhum arquivo selecionado";
    botaoImportar.disabled = true;
    return;
  }

  nomeArquivo.textContent = arquivo.name;
  botaoImportar.disabled = false;

}

document.getElementById("arquivo-importacao").addEventListener("change", arquivoImportacaoSelecionado);
document.getElementById("btn-confirmar-importacao").addEventListener("click", confirmarImportacao);

function selecionarArquivoImportacao() {
  document.getElementById("arquivo-importacao").click();
}

async function importarArquivoAutorizacoes() {
  const input = document.getElementById("arquivo-importacao");
  const arquivo = input.files[0];

  if (!arquivo) {
    return;
  }

  const formData = new FormData();
  formData.append("arquivo", arquivo);

  try {
    const response = await fetch(
      "/autorizacoes/importar",
      {
        method: "POST",
        body: formData
      }
    );

    let resultado;

    try {
      resultado = await response.json();
    } catch (erro) {
      alert("O servidor retornou uma resposta inválida.");
      return;
    }

    if (!response.ok || !resultado.sucesso) {
      alert(resultado.mensagem || "Erro ao importar o arquivo.");
      return;
    }

    resultadoImportacao = resultado;

    preencherResumoImportacao(resultado);
    renderizarTabelaImportacao(resultado);

    fecharModalImportacao();
    abrirModalRevisaoImportacao();

  } catch (erro) {
    console.error("Erro na requisição:", erro);
    alert("Não foi possível comunicar com o servidor.");
  }
}

function baixarModeloImportacao() {
  window.location.href = "/autorizacoes/importacao/modelo";
}

function preencherResumoImportacao(resultado) {

    const totalLinhas = resultado.linhas.length;
    const totalErros = resultado.linhas.filter(linha => !linha.valida,).length;

    document.getElementById("revisao-total-linhas").textContent = `Linhas: ${totalLinhas}`;
    document.getElementById("revisao-total-erros").textContent = `Com erros: ${totalErros}`;

    const divErrosGlobais = document.getElementById("erro-global-importacao");
    divErrosGlobais.textContent = (resultado.erros_globais.length > 0) ?
      resultado.erros_globais[0]: "";

    document.getElementById("btn-confirmar-importacao").disabled = totalErros > 0;
}

function renderizarLinhaImportacao(linha) {

  const autorizacao = linha.autorizacao;
  let situacao;

  if (linha.valida) {
    situacao =`
      <span class="status-importacao-ok">
        ✔ OK
      </span>`;
  } else if (linha.colisao_intervalo) {
    situacao =`
      <span class="status-importacao-erro">
        ❌ Intervalo de tempo inválido.
      </span>`;
  } else {
    situacao =`
      <span class="status-importacao-erro">
        ❌ ${linha.erros.length}
        ${linha.erros.length === 1 ? "erro" : "erros"}
      </span>
      ${renderizarTooltipErros(linha)}`;
  }

  return `
    <tr id="linha-importacao-${linha.numero}">
      <td style="display: none;">${linha.numero}</td>

        ${renderizarCelula(linha, "cpf", autorizacao.cpf)}
        ${renderizarCelula(linha, "nome", autorizacao.nome)}
        ${renderizarCelula(linha, "empresa", autorizacao.empresa)}
        ${renderizarCelula(linha, "placa", autorizacao.placa)}
        ${renderizarCelula(linha, "primeiro_dia", formatarData(autorizacao.primeiro_dia))}
        ${renderizarCelula(linha, "ultimo_dia", formatarData(autorizacao.ultimo_dia))}

      <td class="resultado-importacao">${situacao}</td>
    </tr>`;
}

function renderizarTabelaImportacao(resultado) {

  const tbody = document.getElementById("tbody-importacao");

  tbody.innerHTML = resultado.linhas.sort(
    (a, b) => (a.autorizacao.cpf || "")
      .localeCompare(b.autorizacao.cpf || ""))
      .map(linha => renderizarLinhaImportacao(linha)).join("");
}

function possuiErroCampo(linha, campo,) {
    return linha.erros.some(erro => erro.campo === campo);
}

function renderizarCelula(linha, campo, valor) {

  const bloqueada = resultadoImportacao.erros_globais.length > 0;
  const possuiErro = possuiErroCampo(linha, campo);
  const foiAlterada = linha.campos_alterados.includes(campo);
  const avisoNomeBanco = (campo === "nome" && linha.nome_banco_divergente);

  let classe = "";
  let onclick = "";

  if (!bloqueada) {
    if (possuiErro) {
      classe = "celula-erro";
    } else if (avisoNomeBanco) {
      classe = "celula-aviso";
    } else if (foiAlterada) {
      classe = "celula-corrigida";
    }

    if (avisoNomeBanco) {
      onclick = `onclick="
        mostrarAvisoNomeBanco(${linha.numero})"`;
    } else if (possuiErro || foiAlterada) {
      onclick = `onclick="editarCampoImportacao(${linha.numero}, '${campo}')"`;
    }
  }

  return `
    <td class="${classe}" ${onclick}>
      ${valor ?? ""}
    </td>`;
}

function renderizarTooltipErros(linha,) {

    if (linha.valida) {
      return "";
    }

    return `
        <div class="tooltip-importacao">
            ${linha.erros
                .map(erro => `<div>${erro.mensagem}</div>`)
                .join("")}
        </div>
    `;
}


async function editarCampoImportacao(numeroLinha, campo) {

  const novoValor = prompt("Novo valor:");
  // valorEnviado === novoValor se campo não for de data
  // se campo for data, representação yyyy-mm-dd é feita em valorEnviado
  // dado que esse é o formato reconhecido pelo servidor
  // novoValor representa o novoValor demandado pelo usuário
  // no formado dd/mm/yyyy
  let valorEnviado = novoValor;

  if (campo === "primeiro_dia" || campo === "ultimo_dia") {
    valorEnviado = desformatarData(novoValor);
  }

  if (valorEnviado === null) {
    return;
  }

  const linha = resultadoImportacao.linhas.find(
    linha => linha.numero === numeroLinha);

  linha.autorizacao[campo] = valorEnviado;
  linha.alterada = true;

  if (!linha.campos_alterados.includes(campo)) {
    linha.campos_alterados.push(campo);
  }

  resultadoImportacao.linhas[resultadoImportacao
    .linhas.findIndex(linha => linha.numero === numeroLinha)] = linha;
  
  const camposAlterados = {};
  for (const linhaAtual of resultadoImportacao.linhas) {
    camposAlterados[ linhaAtual.numero ] = [ ...linhaAtual.campos_alterados ];
  }
  
  resultadoImportacao = await revalidarPlanilhaImportacao(resultadoImportacao);
  
  for (const linhaAtual of resultadoImportacao.linhas) {
    linhaAtual.campos_alterados = camposAlterados[linhaAtual.numero] || [];
  }
  
  preencherResumoImportacao(resultadoImportacao);
  renderizarTabelaImportacao(resultadoImportacao);

}

async function revalidarLinhaImportacao(linha) {

  const response = await fetch(
    "/importacao/revalidar-linha", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(linha) });

  const json = await response.json();
  return json;
}

async function confirmarImportacao() {

  const response = await fetch(
    "/importacao/confirmar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(resultadoImportacao) });

  const json = await response.json();

  if (!response.ok) {
    alert(json.detail);
    return;
  }

  await carregarAutorizacoes();

  fecharModalRevisaoImportacao();
  resultadoImportacao = null;

  alert(json.mensagem);
}

async function revalidarPlanilhaImportacao(resultado) {

  const response = await fetch(
    "/importacao/revalidar-planilha", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(resultado) });

  return await response.json();
}

function mostrarAvisoNomeBanco(numeroLinha) {

  const linha = resultadoImportacao.linhas.find(
    linha => linha.numero === numeroLinha);

  alert(
    "Nome informado na planilha:\n\n"
    + linha.nome_planilha

    + "\n\n"

    + "Nome já cadastrado:\n\n"
    + linha.nome_cadastrado

    + "\n\n"

    + "A importação utilizará o nome cadastrado.");
}
