
import { createRouter, createWebHistory } from 'vue-router'
import Home from "../pages/Home.vue";
import OrderCanceled from '../components/OrderCanceled.vue'
import OrderSuccess from '../components/OrderSuccess.vue'


const routes =[
    {
        path:"/",
        name:"home",
        component: Home,
    },
    {
        path: '/success',
        name: 'OrderSuccess',
        component: OrderSuccess,
      },
      {
        path: '/canceled',
        name: 'OrderCanceled',
        component: OrderCanceled,
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