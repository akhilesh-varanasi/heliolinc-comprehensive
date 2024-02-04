<template>
    <nav class="navbar">
      <div class="logo">HelioLinc</div> <!-- Logo added -->
      <ul class="nav-items">
        <li class="nav-item" @click="navigateTo('/')">Home</li>
        <li class="nav-item" @click="navigateTo('/login')">Login/Register</li>
      </ul>
    </nav>
 </template>
  
  
 
 
<script>
    import { defineComponent } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    export default defineComponent({
    name: 'NavBar',
    setup() {
        const router = useRouter();
        const route = useRoute();

        const navigateTo = (path) => {
        if (route.path !== path) {
            router.push(path);
        }
        };

        return { navigateTo };
    }
    });
</script>

 
 
<style>
.navbar {
  display: flex;
  justify-content: flex-start; /* Align items to start */
  align-items: center;
  background-color: #00008B; /* Light blue background */
  padding: 10px 20px;
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
</style>

 
 

