<template>
  <div class="home">
    <div v-if="!isLoggedIn">
      <AuthForm @login-success="handleLoginSuccess" />
    </div>
    <div v-else>
      <CSVSummary />
    </div>
  </div>
</template>

<script setup>
// @ is an alias to /src
import AuthForm from "@/components/AuthForm.vue";
import CSVSummary from "@/views/CSVSummary.vue";
import { inject, defineEmits } from "vue";

const isLoggedIn = inject("isLoggedIn");

const emit = defineEmits(["login-success"]);

function handleLoginSuccess(userData) {
  emit("login-success", userData);
}
</script>
