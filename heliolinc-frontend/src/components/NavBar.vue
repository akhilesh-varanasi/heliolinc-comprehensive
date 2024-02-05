<template>
  <nav class="navbar">
    <div class="logo">HelioLinc</div>
    <div class="spacer" v-if="!isLoggedIn"></div>
    <ul class="nav-items">
      <li class="nav-item" @click="navigateTo('/home')">Home</li>
      <li class="nav-item" @click="navigateTo('/login')">Login / Register</li>
    </ul>
    <button @click="handleSignOut" v-if="isLoggedIn" class="sign-out-btn"> Sign out </button>
  </nav>
</template>
 
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
const router = useRouter();
const route = useRoute();

const navigateTo = (path) => {
    if (route.path !== path) {
        router.push(path);
    }
};

const isLoggedIn = ref(false);
let auth;
onMounted(() => {
  auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      isLoggedIn.value = true;
    } else {
      isLoggedIn.value = false;
    }
  })
});

const handleSignOut = () => {
  signOut(auth).then(() => {
    router.push('/login');
  })
}
</script>


 
 
<style>
.navbar {
  display: flex;
  justify-content: space-between; /* Adjusted to space-between */
  align-items: center;
  background-color: #00008B;
  padding: 10px 20px;
  width: 100%; /* Ensure navbar spans entire width */
}

.logo {
  font-size: 24px; /* Larger font size for the logo */
  font-weight: bold;
  color: #FFFFFF; /* White color for the logo text */
  margin-right: 20px; /* Space between logo and nav items */
}

.nav-items {
  list-style: none;
  display: flex;
  padding: 0;
  margin: 0;
}

.nav-item {
  color: #FFFFFF; /* Light text color */
  padding: 10px 15px;
  margin: 0 10px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.nav-item:hover {
  background-color: #B0C4DE; /* Lighter blue for hover effect */
  border-radius: 5px;
}
.sign-out-btn {
  padding: 10px 15px;
  background-color: #B0C4DE; /* Match the nav-item hover color or any color you prefer */
  color: #FFFFFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.sign-out-btn:hover {
  background-color: #9B30FF; /* Darker blue for hover effect */
}

.spacer {
  flex-grow: 1;
}

</style>

 
 

