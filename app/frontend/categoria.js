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
    }
 })
 
 
 