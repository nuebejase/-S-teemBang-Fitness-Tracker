import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
} from 'vue-router'
import { useAppStore } from '@/stores/appStore'
import Layout from '@/components/Layout.vue'
import Home from '@/pages/Home.vue'
import Products from '@/pages/Products.vue'
import Cart from '@/pages/Cart.vue'
import Checkout from '@/pages/Checkout.vue'
import Orders from '@/pages/Orders.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import Profile from '@/pages/Profile.vue'
import About from '@/pages/About.vue'
import AdminDashboard from '@/pages/admin/AdminDashboard.vue'
import AdminProducts from '@/pages/admin/AdminProducts.vue'
import AdminOrders from '@/pages/admin/AdminOrders.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', name: 'home', component: Home },
        { path: 'products', name: 'products', component: Products },
        { path: 'cart', name: 'cart', component: Cart },
        {
          path: 'checkout',
          name: 'checkout',
          component: Checkout,
          meta: { requiresAuth: true, requiresCustomer: true },
        },
        {
          path: 'orders',
          name: 'orders',
          component: Orders,
          meta: { requiresAuth: true, requiresCustomer: true },
        },
        {
          path: 'profile',
          name: 'profile',
          component: Profile,
          meta: { requiresAuth: true },
        },
        { path: 'about', name: 'about', component: About },
        { path: 'contact', name: 'contact', component: About },
        {
          path: 'admin',
          name: 'admin',
          component: AdminDashboard,
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'admin/products',
          name: 'admin-products',
          component: AdminProducts,
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'admin/orders',
          name: 'admin-orders',
          component: AdminOrders,
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'admin/profile',
          name: 'admin-profile',
          component: Profile,
          meta: { requiresAuth: true, requiresAdmin: true },
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guestOnly: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

router.beforeEach((to: RouteLocationNormalized) => {
  const appStore = useAppStore()
  const user = appStore.user

  if (to.meta.guestOnly && user) {
    return { path: user.role === 'admin' ? '/admin' : '/' }
  }

  if (to.meta.requiresAuth && !user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return { name: 'home' }
  }

  if (to.meta.requiresCustomer && user?.role === 'admin') {
    return { name: 'admin' }
  }

  return true
})

export default router
