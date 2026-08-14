async function buscarConfiguracaoPainel() {

  const response = await fetch("/painel-autorizacao/configuracao");
  if (!response.ok) {
    const texto = await response.text();
    console.error(texto);
    throw new Error("Erro ao buscar a configuração do painel.");
  }

  return await response.json();
}

async function iniciarAtualizacaoAutomatica() {

  const configuracao = await buscarConfiguracaoPainel();
  const intervalo = Number(configuracao.refresh_ms);

  if (intervalo <= 0) {
    return;
  }

  setInterval(carregarPainel, intervalo);
}
