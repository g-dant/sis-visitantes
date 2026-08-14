async function encerrarSessao(confirmar = true) {

  if (confirmar && !confirm("Deseja realmente sair?")) {
    return;
  }

  try {

    const response = await fetch("/logout", {
      method: "POST"
    });

    if (!response.ok) {
      throw new Error("Erro ao encerrar sessão.");
    }

    window.location.href = "/";

  } catch (error) {

    console.error(error);
    alert("Não foi possível encerrar a sessão.");

  }
}
