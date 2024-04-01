import './style.css'
import App from './App.vue'
import router from "./routes/index.js"
import { createApp,markRaw  } from 'vue'

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia().use(({ store }) => {
    store.$router = markRaw(router)
  });
  pinia.use(piniaPluginPersistedstate)
createApp(App).use(pinia).use(router).mount('#app')