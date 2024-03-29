import { createRouter, createWebHistory } from 'vue-router'
import PoolPage from "../pages/PoolPage.vue";
import OrderCanceled from '../components/OrderCanceled.vue'
import OrderSuccess from '../components/OrderSuccess.vue'
import Login from "../pages/Login.vue"
import IndividualPoolPage from "../pages/IndividualPoolPage.vue"
import PoolFormCreation from "../pages/PoolFormCreation.vue"
import Register from "../pages/Register.vue"
import PoolInvite from "../pages/PoolInvite.vue"
import OwnerPoolPage from "../pages/OwnerPoolPage.vue"
import HomePage from "../pages/Home.vue"



const routes =[
    {
        path:"/",
        name:"PoolPage",
        component: PoolPage,
    },
    {
      path:"/home",
      name:"HomePage",
      component: HomePage,
    },
    {
      path: "/register",
      name: "Register",
      component: Register,
    },
    {
      path: "/poolinvite",
      name: "PoolInvite",
      component: PoolInvite,
    },
    {
      path: "/poolcreation",
      name: "PoolFormCreation",
      component: PoolFormCreation,
    },
    
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/ipp",
      name: "IndividualPoolPage",
      component: IndividualPoolPage,
    },
    {
      path: "/opp",
      name: "OwnerPoolPage",
      component: OwnerPoolPage,
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