async function carregarPainel() {

  const response = await fetch("/painel-autorizacao");

  if (!response.ok) {
    console.error("Erro ao carregar painel");
    return;
  }

  const painel = await response.json();
  atualizarPainel(painel);
}

function atualizarPainel(painel) {

  const ids = {
    "Autorizada": "painel-autorizadas",
    "Pendente": "painel-pendentes",
    "Revogada": "painel-revogadas",
    "Expirada": "painel-expiradas"
  };

  for (const item of painel) {

    const id = ids[item.status_exibicao];

    if (id) {
      document.getElementById(id).innerText = item.quantidade;
    }
  }
}

