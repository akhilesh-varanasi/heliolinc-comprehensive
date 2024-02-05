import App from './App.vue'

import vuetify from './plugins/vuetify'
import {createApp } from 'vue'
import router from '@/router/router.js'
import 'vuetify/styles' // Import Vuetify styles
import { createVuetify } from 'vuetify'
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA1Xx9GYNjf7_zaxRLo2yFbSLWh_K1XAFc",
  authDomain: "heliolinc-app.firebaseapp.com",
  projectId: "heliolinc-app",
  storageBucket: "heliolinc-app.appspot.com",
  messagingSenderId: "469909726801",
  appId: "1:469909726801:web:f6ef9c9cf9f871a0a7fa70",
  measurementId: "G-JFTRP99C0F"
};

export default createVuetify()
initializeApp(firebaseConfig);
const app = createApp(App)

app
   .use(router)
   .use(vuetify)
   .mount('#app')