const API_URL_CAT = "http://localhost:8000/categorias";

//verificacion de TOKEN
 
document.getElementById('categoria_form').addEventListener('submit',async function(e) {
    e.preventDefault();
    const data = {
    nombre: document.getElementById("nombre_categoria").value,
    descripcion: document.getElementById("descripcion_categoria").value};
    const res = await fetch(API_URL_CAT, {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
    if (!res.ok){
        const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
        alert("Error: " + err.detail);
    }else{
      alert(data?.detail || "Creacion de categoria exitosa!");
      cargarCategorias()
      document.getElementById("categoria_form").reset()
    }
 })
 
async function cargarCategorias() {
const res = await fetch(`${API_URL_CAT}/getCategorias`);

if (!res.ok) {
  alert("Error al cargar categorias");
  return;
  }else{
  const categorias = await res.json();
  const contenedor = document.getElementById("insertar-categorias"); //tomo contenedor de categorias
  contenedor.innerHTML = "";  //lo limpio , sirve para actualizar tmb esta funcion
  categorias.forEach((categoria) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span> <strong> ID: ${categoria.id} </strong> ${categoria.nombre} – ${categoria.descripcion}</span>
        <div>
        <button onclick="borrarCategoria(${categoria.id})">Eliminar</button>
        </div>
      `;
      contenedor.appendChild(li);
    })
  document.getElementById()

  }
}
cargarCategorias()

async function borrarCategoria(id){
const res = await fetch(`${API_URL_CAT}/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });
if (!res.ok){
  alert("Error al cargar categorias");
  return;
}else{
  cargarCategorias()
  return alert('Categoria eliminada con exito!')
}
}