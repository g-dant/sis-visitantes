let leitorQrCode = null;
let leituraQrCodeEmAndamento = null;

function abrirModalQrCode() {
  document.getElementById("modalQrCode").style.display = "flex";
}

function fecharModalQrCode() {
  document.getElementById("qrcode-imagem").innerHTML = "";
  document.getElementById("modalQrCode").style.display = "none";
}

async function qrCodeLido(textoQrCode) {

  if (leituraQrCodeEmAndamento) {
    return
  }
  leturaQrCodeEmAndamento = true;

  await fecharLeitorQrCode();

  const tokenQrCode = extrairTokenQrCode(textoQrCode);
  const response = await fetch(`/verificar/${tokenQrCode}`);
  if (!response.ok) {
    alert("QR Code inválido.");
    return;
  }

  const autorizacao = await response.json();
  await exibirAutorizacaoEmModoVisualizacao(autorizacao);
}

async function abrirLeitorQrCode() {
  document.getElementById("modalLeitorQrCode").style.display = "flex";
  leitorQrCode = new Html5Qrcode("reader");
  await leitorQrCode.start(
    { facingMode: "environment" },
    { fps: 10, qrbox: 250 },
    qrCodeLido
  );
}

async function fecharLeitorQrCode() {
  if (leitorQrCode) {
    try {
      await leitorQrCode.stop();
    } catch (e) { /* SCANNER JÁ PARADO */ }
    leitorQrCode = null;
  }

  document.getElementById("modalLeitorQrCode").style.display = "none";
}

async function visualizarQrCode() {

  const response = await fetch(
    `/autorizacoes/${idAutorizacaoVisualizada}/qrcode`);

  if (!response.ok) {
    alert("Erro ao gerar QR Code.");
    return;
  }

  const dados = await response.json();
  renderizarQrCode(dados.url);
  abrirModalQrCode();
}

function renderizarQrCode(url) {

  const container = document.getElementById("qrcode-imagem");
  container.innerHTML = "";

  new QRCode(
    container, {
      text: url,
      width: 300,
      height: 300
    });
}

function imprimirQrCode() {

  const img = document.querySelector("#qrcode-imagem img");
  const janela = window.open("", "_blank");

  janela.document.write(`
    <html>
      <head>
        <title>QR Code</title>
        <style>
          body {
            font-family: Arial;
            text-align: center;
            margin-top: 40px;
          }
          img {
            width: 320px;
            height: 320px;
          }
          p {
            margin-top: 25px;
            font-size: 18px;
          }
        </style>
      </head>
      <body>
        <h2>QR Code da Autorização</h2>
        <img src="${img.src}">
        <p>Apresente este QR Code na portaria.</p>
      </body>
    </html>
  `);

  janela.document.close();
  janela.focus();
  janela.print();
  janela.close();
}

// Funções de leitura e processamento do QR CODE
function extrairTokenQrCode(url) {
  const caminho = new URL(url, window.location.origin).pathname;
  return caminho.split("/").pop();
}

function atualizarStatusDestaque(autorizacao, exibir = true) {

  const painel = document.getElementById("status-autorizacao-destaque");

  if (!exibir) {
    painel.style.display = "none";
    return;
  }

  const texto = document.getElementById("status-autorizacao-texto");

  painel.className = "status-autorizacao-destaque";
  painel.classList.add(cores_status[ autorizacao.status_exibicao ]);
  texto.textContent = autorizacao.status_exibicao.toUpperCase();
  painel.style.display = "block";

}

// Melhorar legibiliade das chamadas de função
function exibirStatusDestaque(autorizacao) { atualizarStatusDestaque(autorizacao, true); }
function ocultarStatusDestaque(autorizacao) { atualizarStatusDestaque(autorizacao, false); }
