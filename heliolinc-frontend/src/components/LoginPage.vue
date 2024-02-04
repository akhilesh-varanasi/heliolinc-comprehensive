<template>
  <nav-bar />
  <div class="login-register-container">
    <div class="login-register-box">
      <h2>{{ isLoginMode ? 'Login' : 'Register' }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="input-field">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required>
        </div>

        <div class="input-field">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
        </div>

        <button type="submit">{{ isLoginMode ? 'Login' : 'Register' }}</button>
        <button type="button" @click="toggleMode">
          {{ isLoginMode ? 'Need an account? Register' : 'Have an account? Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'LoginRegister',
  setup() {
    const isLoginMode = ref(true);
    const username = ref('');
    const password = ref('');

    const toggleMode = () => {
      isLoginMode.value = !isLoginMode.value;
    };

    const handleSubmit = () => {
      // Placeholder for authentication logic
      console.log('Submitted:', { username: username.value, password: password.value });
    };

    return { isLoginMode, username, password, toggleMode, handleSubmit };
  },
});
</script>

<style scoped>
.login-register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full viewport height */
  background-color: #f5f5f5;
}

.login-register-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.input-field {
  margin-bottom: 20px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #4A90E2;
  color: white;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #3a78c7;
}
</style>
