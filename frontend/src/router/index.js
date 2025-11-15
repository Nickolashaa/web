import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Shop from '../views/Shop.vue'
import Cart from '../views/Cart.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/shop',
    name: 'Shop',
    component: Shop,
    meta: { requiresAuth: true }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin) {
    if (user) {
      const userData = JSON.parse(user)
      if (userData.is_superuser) {
        next()
      } else {
        next('/shop')
      }
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
