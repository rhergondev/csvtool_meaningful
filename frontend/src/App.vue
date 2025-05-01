<template>
  <header class="app-header">
    <div class="app-title">CSV TOOL</div>
    <nav class="user-nav">
      <template v-if="isLoggedIn">
        <span>Welcome, {{ username }}</span>
        <button @click="handleLogout" class="logout-button">Logout</button>
      </template>
    </nav>
  </header>
  <router-view @login-success="fetchUserStatus" />
</template>

<script setup>
import { ref, onMounted, provide, readonly } from "vue";

const isLoggedIn = ref(false);
const username = ref(null);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function fetchUserStatus() {
  console.log("Fetching user status...");
  try {
    const response = await fetch("/api/users/status/", {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      isLoggedIn.value = data.isAuthenticated;
      username.value = data.user;
    } else {
      console.error("Error fetching user status:", response.statusText);
    }
  } catch (error) {
    console.error("Error fetching user status:", error);
  }
}

async function handleLogout() {
  const csrftoken = getCookie("csrftoken");

  if (!csrftoken) {
    console.error("CSRF token not found");
    return;
  }

  try {
    const response = await fetch("/api/users/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    });

    if (response.ok) {
      isLoggedIn.value = false;
      username.value = null;
      console.log("Logout successful");
    } else {
      console.error("Error during logout:", response.statusText);
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
}

provide("isLoggedIn", readonly(isLoggedIn));
provide("currentUserState", readonly(username));

onMounted(() => {
  fetchUserStatus();
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 20px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

<style scoped>
.app-header {
  display: flex; /* Activa Flexbox */
  justify-content: space-between; /* Empuja título a la izq y nav a la der */
  align-items: center; /* Centra verticalmente los items */
  padding: 1rem 2rem; /* Padding vertical y horizontal */
  background-color: #f8f9fa; /* Un color de fondo suave (puedes cambiarlo) */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.app-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.user-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  font-weight: bold;
  color: #555;
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: #6790fc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.2s ease;
}

.logout-button:hover {
  background-color: #5174cd; /* Un azul un poco más oscuro al pasar el ratón */
}
</style>
