const API_URL_REGISTRO = "http://localhost:8000/auth";



document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();


    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;
    const nombre = document.getElementById("nombre").value;
  try {
    const res = await fetch(`${API_URL_REGISTRO}/registro`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre,email, contraseña: password, rol }),
    });

    const messageDiv = document.getElementById("message");

    if (!res.ok) {
      const error = await res.json();
      messageDiv.innerText = error.detail || "Error al registrar";
      messageDiv.style.display = "block";
      return;
    }

    messageDiv.innerText = "Usuario registrado con éxito";
    messageDiv.style.display = "block";
  } catch (err) {
    console.error(err);
    alert("Error de conexión con el servidor");
  }
});