const input = document.getElementById("buscador");
const contenedor = document.getElementById("eventosDisponibles");

document.addEventListener("keyup", (e) => {
  if (e.target.matches("#buscador")) {
    const eventos = document.querySelectorAll(".evento");
    let visibles = 0;

    eventos.forEach((evento) => {
      const texto = evento.textContent.toLowerCase();
      const filtro = e.target.value.toLowerCase();

      if (texto.includes(filtro)) {
        evento.parentElement.style.display = "block";
        visibles++;
      } else {
        evento.parentElement.style.display = "none";
      }
    });

    // Mostrar o eliminar mensaje si no hay coincidencias
    let mensaje = document.getElementById("sinResultados");

    if (visibles === 0) {
      if (!mensaje) {
        mensaje = document.createElement("li");
        mensaje.id = "sinResultados";
        mensaje.textContent = "No se encontraron eventos";
        contenedor.appendChild(mensaje);
      }
    } else {
      if (mensaje) mensaje.remove();
    }
  }
});
