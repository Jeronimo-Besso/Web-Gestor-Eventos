const API_EVENTOS = "http://localhost:8000/eventos";
const API_INSCRIPCIONES = "http://localhost:8000/inscripciones";
const token = localStorage.getItem("token");
let inscripcionesActivas = [];

// Redirige si no hay token
if (!token) {
  alert("No estás logueado. Redirigiendo...");
  window.location.href = "login.html";
}

// Cargar eventos disponibles (excluyendo los ya inscritos)
async function cargarEventos() {
  const res = await fetch(API_EVENTOS);
  const eventos = await res.json();

  const lista = document.getElementById("eventosDisponibles");
  lista.innerHTML = "";

  eventos.forEach((evento) => {
    const yaInscripto = inscripcionesActivas.some(
      (insc) => insc.evento && insc.evento.id === evento.id
    );
    if (yaInscripto) return;

    const item = document.createElement("li");
    item.innerHTML = `
      <div>
        <strong>${evento.nombre}</strong>
        <p>${evento.descripcion}</p>
        <p><small>Del ${evento.fecha_inicio} al ${evento.fecha_fin}</small></p>
        <button onclick="inscribirse(${evento.id})">Inscribirme</button>
      </div>
    `;
    lista.appendChild(item);
  });
}

// Inscribirse a un evento
async function inscribirse(eventoId) {
  try {
    const res = await fetch(API_INSCRIPCIONES, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ evento_id: Number(eventoId) }),
    });

    let data = null;
    try {
      data = await res.json();
    } catch (err) {}

    if (!res.ok) {
      alert(data?.detail || "No se pudo inscribir.");
    } else {
      alert(data?.detail || "¡Inscripción exitosa!");
      refrescarUI();
    }
  } catch (error) {
    console.error("Error al inscribirse:", error);
    alert("Error de conexión al inscribirse.");
  }
}

// Desinscribirse de un evento
async function desinscribirse(eventoId) {
  if (!confirm("¿Seguro que querés desinscribirte?")) return;

  try {
    const res = await fetch(`${API_INSCRIPCIONES}/${eventoId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    let data = null;
    try {
      data = await res.json();
    } catch (err) {}

    if (!res.ok) {
      alert(data?.detail || "No se pudo desinscribir.");
    } else {
      alert(data?.detail || "Desinscripción exitosa.");
      refrescarUI();
    }
  } catch (error) {
    console.error("Error al desinscribirse:", error);
    alert("Error de conexión al desinscribirse.");
  }
}

// Cargar inscripciones activas
async function cargarInscripcionesActivas() {
  const res = await fetch(`${API_INSCRIPCIONES}/activas`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await res.json();

  if (!Array.isArray(data)) {
    console.error("No llegó una lista:", data);
    alert(data.detail || "Error al cargar inscripciones.");
    return;
  }

  inscripcionesActivas = data;

  const contenedor = document.getElementById("inscripcionesActivas");
  contenedor.innerHTML = "";

  data.forEach((insc) => {
    if (!insc.evento) return;

    const item = document.createElement("li");
    item.innerHTML = `
      <div>
        <strong>${insc.evento.nombre}</strong>
        <p><small>Del ${insc.evento.fecha_inicio} al ${insc.evento.fecha_fin}</small></p>
        <button onclick="desinscribirse(${insc.evento.id})">Desinscribirse</button>
      </div>
    `;
    contenedor.appendChild(item);
  });
}

fetch("http://localhost:8000/inscripciones/historial", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
  .then(res => {
    if (!res.ok) throw new Error("Error al obtener historial");
    return res.json();
  })
  .then(historial => mostrarHistorial(historial))
  .catch(error => {
    console.error(error);
    alert("Hubo un error al cargar el historial");
  });

function mostrarHistorial(historial) {
  const tbody = document.querySelector("#tablaHistorial tbody");
  tbody.innerHTML = ""; // Limpiar por si ya había datos

  historial.forEach(inscripcion => {
    const tr = document.createElement("tr");

    const tdEvento = document.createElement("td");
    tdEvento.textContent = inscripcion.evento.nombre;

    const tdInicio = document.createElement("td");
    tdInicio.textContent = inscripcion.evento.fecha_inicio;

    const tdFin = document.createElement("td");
    tdFin.textContent = inscripcion.evento.fecha_fin;

    const tdFechaInscripcion = document.createElement("td");
    tdFechaInscripcion.textContent = inscripcion.fecha_inscripcion;

    tr.appendChild(tdEvento);
    tr.appendChild(tdInicio);
    tr.appendChild(tdFin);
    tr.appendChild(tdFechaInscripcion);

    tbody.appendChild(tr);
  });
}

function cargarHistorial() {
  fetch("http://localhost:8000/inscripciones/historial", {
    method: "GET",
    headers: { "Authorization": `Bearer ${token}` }
  })
    .then(res => {
      if (!res.ok) throw new Error("Error al obtener historial");
      return res.json();
    })
    .then(historial => mostrarHistorial(historial))
    .catch(error => {
      console.error(error);
      alert("Hubo un error al cargar el historial");
    });
}


const headers = { Authorization: `Bearer ${token}` };

fetch("http://localhost:8000/dashboard/total-eventos", { headers })
  .then(res => res.json())
  .then(data => document.getElementById("totalEventos").textContent = data.total_eventos);

fetch("http://localhost:8000/dashboard/inscripciones-activas", { headers })
  .then(res => res.json())
  .then(data => document.getElementById("inscripcionesActivasNav").textContent = data.inscripciones_activas);

fetch("http://localhost:8000/dashboard/promedio-inscriptos", { headers })
  .then(res => res.json())
  .then(data => document.getElementById("promedio").textContent = data.promedio_inscriptos_por_evento);

fetch("http://localhost:8000/dashboard/evento-mas-inscripciones", { headers })
  .then(res => res.json())
  .then(data => {
    if (data.nombre) {
      document.getElementById("masPopular").textContent = data.nombre;
      document.getElementById("cantPopular").textContent = data.inscripciones;
    } else {
      document.getElementById("masPopular").textContent = "Ninguno";
      document.getElementById("cantPopular").textContent = "0";
    }
  });

// Refrescar UI completa
function refrescarUI() {
  cargarInscripcionesActivas();
  cargarEventos();
  cargarHistorial();
}

// Inicializar al entrar
refrescarUI();