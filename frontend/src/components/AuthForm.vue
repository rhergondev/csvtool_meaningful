<template>
  <div class="auth-form">
    <!------ Login Form ------->
    <div v-if="isLogin">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div>
          <label for="login-password">Password</label>
          <input
            :type="showPassword ? 'text' : 'password'"
            id="login-password"
            v-model="password"
            required
          />
        </div>
        <div>
          <label for="show-password">Show Password</label>
          <input type="checkbox" id="show-password" v-model="showPassword" />
        </div>
        <button type="submit">Login</button>
      </form>
      <p @click="toggleForm">Need an account? Register</p>
    </div>
    <!------- Registration Form -------->
    <div v-else>
      <h2>Register</h2>
      <form @submit.prevent="handleRegister">
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div>
          <label for="register-password">Password</label>
          <input
            :type="showPassword ? 'text' : 'password'"
            id="register-password"
            v-model="password"
            required
          />
        </div>
        <div>
          <label for="confirm-password">Confirm Password</label>
          <input
            :type="showPassword ? 'text' : 'password'"
            id="confirm-password"
            v-model="passwordConfirm"
            required
          />
        </div>
        <div>
          <label for="show-password">Show Password</label>
          <input type="checkbox" id="show-password" v-model="showPassword" />
        </div>
        <button type="submit">Register</button>
      </form>
      <p @click="toggleForm">Already have an account? Login</p>
    </div>
    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    <p v-if="isLoading">Loading...</p>
    <p v-if="successMsg" class="success">{{ successMsg }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from "vue";

const emit = defineEmits(["login-success"]);

onMounted(async () => {
  try {
    await fetch("/api/users/status/", {
      credentials: "include",
    });
  } catch (error) {
    console.error("Error fetching status:", error);
    errorMsg.value =
      "Error fetching status. Please check your server connection.";
  }
});

const showPassword = ref(false);
const isLogin = ref(true);

const username = ref("");
const password = ref("");
const passwordConfirm = ref("");

const isLoading = ref(false);
const errorMsg = ref("");
const successMsg = ref("");

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

function toggleForm() {
  isLogin.value = !isLogin.value;

  username.value = "";
  password.value = "";
  passwordConfirm.value = "";
  errorMsg.value = "";
  isLoading.value = false;
}

async function handleLogin() {
  isLoading.value = true;
  errorMsg.value = "";
  successMsg.value = "";
  const csrftoken = getCookie("csrftoken");

  if (!csrftoken) {
    errorMsg.value = "CSRF token not found. Reload the page.";
    isLoading.value = false;
    return;
  }

  try {
    const response = await fetch("/api/users/login/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.error || `Error ${response.status}: ${response.statusText}`
      );
    }

    console.log("Login successful:", data);
    successMsg.value = `Welcome ${data.user}!`;
    username.value = "";
    password.value = "";
    passwordConfirm.value = "";

    console.log("Login successful:", data.user);
    emit("login-success", data.user);
  } catch (error) {
    console.error("Login failed", error);
    errorMsg.value = error.message || "An error occurred during login.";
  } finally {
    isLoading.value = false;
  }
}

async function handleRegister() {
  if (password.value !== passwordConfirm.value) {
    errorMsg.value = "Passwords do not match.";
    return;
  }
  isLoading.value = true;
  errorMsg.value = "";
  successMsg.value = "";
  const csrftoken = getCookie("csrftoken");

  if (!csrftoken) {
    errorMsg.value = "CSRF token not found. Reload the page.";
    isLoading.value = false;
    return;
  }

  try {
    const response = await fetch("/api/users/register/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.error || `Error ${response.status}: ${response.statusText}`
      );
    }

    console.log("Registration successful:", data);
    successMsg.value = `Welcome ${data.user}!`;
    username.value = "";
    password.value = "";
    passwordConfirm.value = "";
    emit("login-success", data.user);
  } catch (error) {
    console.error("Registration failed", error);
    errorMsg.value = error.message || "An error occurred during registration.";
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.auth-form h2 {
  text-align: center;
}
.auth-form form {
  display: flex;
  flex-direction: column;
}
.auth-form form div {
  margin-bottom: 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.auth-form form label {
  margin-bottom: 5px;
}
.auth-form form input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 60%;
}
.auth-form form button {
  padding: 10px;
  background-color: #6790fc;
  color: white;
  font-weight: 800;
  text-transform: uppercase;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.auth-form form button:hover {
  background-color: #5174cd;
}
.auth-form p {
  text-align: center;
  cursor: pointer;
  color: #007bff;
}
p.error {
  color: red;
  text-align: center;
}
p.success {
  color: green;
  text-align: center;
}
</style>
