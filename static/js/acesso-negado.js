document.getElementById("btn-escanear-qrcode").style.display = "none";
document.getElementById("btn-retornar-login").
  addEventListener("click", function(event) {
    event.preventDefault();
    encerrarSessao(false);
})
