import './style.css'
import App from './App.vue'
import router from "./routes/index.js"
import { createApp,markRaw  } from 'vue'


createApp(App).use(router).mount('#app')