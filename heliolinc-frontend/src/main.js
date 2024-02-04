import App from './App.vue'

import vuetify from './plugins/vuetify'
import {createApp } from 'vue'
import createRouter from './router/router.js'
import 'vuetify/styles' // Import Vuetify styles
import { createVuetify } from 'vuetify'

export default createVuetify() // Replaces new Vuetify(...)
const app = createApp(App)
const router = createRouter()

app
   .use(router)
   .use(vuetify)
   .mount('#app')