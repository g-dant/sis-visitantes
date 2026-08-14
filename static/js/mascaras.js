function mascararCpf(event) {

  let valor = event.target.value.replace(/\D/g, "");

  valor = valor.substring(0, 11);
  valor = valor.replace(/^(\d{3})(\d)/, "$1.$2");
  valor = valor.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
  valor = valor.replace(/\.(\d{3})(\d)/, ".$1-$2");

  event.target.value = valor;
}

function mascararRg(event) {

  let valor = event.target.value.replace(/\D/g, "");

  valor = valor.substring(0, 9);
  valor = valor.replace(/^(\d{2})(\d)/, "$1.$2");
  valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
  valor = valor.replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");

  event.target.value = valor;
}

function mascararPlaca(event) {

  let valor = event.target.value.replace(/[^A-Za-z0-9]/g, "").toUpperCase();

  valor = valor.substring(0, 7);
  event.target.value = valor;
}

function mascararCelular(event) {

  let valor = event.target.value.replace(/[^\d]/g, "");

  if (valor.startsWith("55")) {
    valor = valor.substring(2);
  }

  valor = valor.substring(0, 11);

  let resultado = "+55 ";
  if (valor.length > 0) {
    resultado += "(" + valor.substring(0, 2);
    if (valor.length >= 2) {
      resultado += ")";
    }
  }

  if (valor.length > 2) {
    resultado += " " + valor.substring(2, 7);
  }

  if (valor.length > 7) {
    resultado += "-" + valor.substring(7, 11);
  }

  event.target.value = resultado;
}

