
import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/Home.vue";

const routes =[
    {
        path:"/",
        name:"home",
        component: Home,
    },

]

const router = createRouter({
    mode: "history",
    base: '/',
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

// router.beforeEach(async (to) => {
//     // clear alert on route change

//   })

export default router