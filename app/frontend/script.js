const API_URL = "http://localhost:8000/eventos";

// Obtener token del localStorage
const token = localStorage.getItem("token");

// Redirigir si no hay token
if (!token) {
  alert("No estás logueado. Redirigiendo al login...");
  window.location.href = "http://127.0.0.1:5500/app/frontend/lofin.html";
}

// Cargar eventos
async function cargarEventos() {
  const res = await fetch(API_URL);
  if (!res.ok) {
    alert("Error al cargar eventos");
    return;
  }

  const eventos = await res.json();
  const lista = document.getElementById("listaEventos");
  lista.innerHTML = "";

  eventos.forEach((evento) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span><strong>${evento.nombre}</strong> – ${evento.descripcion}</span>
      <div>
      <button onclick="borrarEvento(${evento.id})">Eliminar</button>
      <button class="editar" onclick="cargarFormulario(${evento.id})">Editar</button>
      </div>
    `;
    lista.appendChild(li);
  });
}

// Precargar formulario para edición
async function cargarFormulario(id) {
  const res = await fetch(`${API_URL}/${id}`);
  if (!res.ok) {
    alert("Error al cargar el evento.");
    return;
  }

  const evento = await res.json();
  document.getElementById("nombre").value = evento.nombre;
  document.getElementById("descripcion").value = evento.descripcion;
  document.getElementById("fecha_inicio").value = evento.fecha_inicio;
  document.getElementById("fecha_fin").value = evento.fecha_fin;
  document.getElementById("lugar").value = evento.lugar;
  document.getElementById("cupos").value = evento.cupos;
  document.getElementById("categoria_id").value = evento.categoria_id;
  document.getElementById("boton").textContent = "Editar Evento"
  document.getElementById("eventoForm").dataset.editando = id;
}

// Crear o actualizar evento
document.getElementById("eventoForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const idEditando = document.getElementById("eventoForm").dataset.editando;
  const url = idEditando ? `${API_URL}/${idEditando}` : API_URL;
  const metodo = idEditando ? "PUT" : "POST";

  const data = {
    nombre: document.getElementById("nombre").value,
    descripcion: document.getElementById("descripcion").value,
    fecha_inicio: document.getElementById("fecha_inicio").value,
    fecha_fin: document.getElementById("fecha_fin").value,
    lugar: document.getElementById("lugar").value,
    cupos: parseInt(document.getElementById("cupos").value),
    categoria_id: parseInt(document.getElementById("categoria_id").value)
  };

  const res = await fetch(url, {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data),
  });

  if (res.ok) {
    alert(idEditando ? "Evento actualizado!" : "Evento creado!");
    document.getElementById("boton").textContent = "Crear Evento"
    document.getElementById("eventoForm").reset();
    delete document.getElementById("eventoForm").dataset.editando;
    cargarEventos();
  } else {
    const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
    alert("Error: " + err.detail);
  }
});

// Borrar evento
async function borrarEvento(id) {
  const confirmacion = confirm("¿Eliminar este evento?");
  if (!confirmacion) return;

  const res = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });

  if (res.ok) {
    alert("Evento eliminado");
    cargarEventos();
  } else {
    const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
    alert("Error al eliminar: " + err.detail);
  }
}

// Inicializar
cargarEventos();