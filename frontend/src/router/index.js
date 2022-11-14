import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
    {
        path: '/',
        name: 'HomeView',
        component: HomeView
    },
    {
        path: '/login',
        name: 'LogIn',
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/sign-up',
        name: 'SignUp',
        component: () => import('../views/RegisterView.vue')
    },
    {
        path: '/stocks',
        name: 'StockPrices',
        component: () => import('../views/StockPricesView.vue')
    },
    {
        path: '/password/reset',
        name: 'ForgotPassword',
        component: () => import('../views/ForgotPasswordView.vue')
    },
    {
        path: '/password/set/:uidb/:token',
        name: 'PasswordSet',
        component: () => import('../views/PasswordSetView.vue')
    },
    {
      path: '/activate/:uidb/:token',
      name: 'ActivateAccount',
      component: () => import('../views/ActivateAccountView.vue')
    },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
