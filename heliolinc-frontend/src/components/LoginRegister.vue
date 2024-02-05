<template>
  <div class="login-register-container">
    <div class="login-register-box">
      <h2>{{ isLoginMode ? 'Login' : 'Register' }}</h2>

      <form @submit.prevent="handleSubmit">
        <div class="input-field">
          <label for="email">Email</label>
          <input type="text" id="email" v-model="email" required placeholder="Enter your email">
        </div>

        <div class="input-field">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required placeholder="Enter your password">
        </div>

        <p v-if="errMsg" class="error-message">{{ errMsg }}</p>

        <button type="submit">{{ isLoginMode ? 'Login' : 'Register' }}</button>
        <button type="button" @click="toggleMode" class="toggle-button">
          {{ isLoginMode ? 'Need an account? Register' : 'Have an account? Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import NavBar from './NavBar.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

const router = useRouter();
const auth = getAuth();
const isLoginMode = ref(true);
const email = ref('');
const password = ref('');
const errMsg = ref('');

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value;
  errMsg.value = '';
};

const handleSubmit = async () => {
  try {
    if (isLoginMode.value) {
      await signInWithEmailAndPassword(auth, email.value, password.value);
    } else {
      await createUserWithEmailAndPassword(auth, email.value, password.value);
    }
    router.push('/home');
  } catch (error) {
      console.log(error.code);
      switch (error.code) {
        case "auth/invalid-email":
          errMsg.value = "Invalid email";
          break;
        case "auth/user-not-found":
          errMsg.value = "No account with that email was found";
          break;
        case "auth/wrong-password":
          errMsg.value = "Incorrect password";
          break;
        default:
          errMsg.value = "Email or password was incorrect";
          break;
      }
  }
};

// const signInWithGoogle = async () => {
//   const provider = new GoogleAuthProvider();
//   try {
//     await signInWithPopup(auth, provider);
//     router.push('/');
//   } catch (error) {
//     errMsg.value = error.message;
//   }
// };
</script>

<style scoped>
.login-register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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

.error-message {
  color: red;
  margin-bottom: 10px;
}

.toggle-button {
  background-color: #f5f5f5;
  color: #4A90E2;
  margin-top: 20px;
}
</style>
