<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import { useAppStore } from '@/stores/appStore'
import {
  ShoppingCart,
  User,
  Home,
  Package,
  LogOut,
  BarChart3,
  Menu,
  X,
} from 'lucide-vue-next'

const appStore = useAppStore()
const route = useRoute()
const router = useRouter()

const mobileMenuOpen = ref(false)

const user = computed(() => appStore.user)
const cartItemCount = computed(() => appStore.cartItemCount)

const isActive = (path: string) => route.path === path

const customerLinks = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/products', label: 'Products', icon: Package },
]

const adminLinks = [
  { path: '/admin', label: 'Dashboard', icon: BarChart3 },
  { path: '/admin/products', label: 'Products', icon: Package },
  { path: '/admin/orders', label: 'Orders', icon: ShoppingCart },
]

const links = computed(() =>
  user.value?.role === 'admin' ? adminLinks : customerLinks,
)

const handleLogout = () => {
  appStore.logout()
  router.push('/')
  mobileMenuOpen.value = false
}

const closeMobile = () => {
  mobileMenuOpen.value = false
}

const profilePath = computed(() =>
  user.value?.role === 'admin' ? '/admin/profile' : '/profile',
)
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background">
    <header
      class="bg-white border-b-2 border-pink-200 sticky top-0 z-50 shadow-sm"
    >
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <RouterLink to="/" class="flex items-center space-x-2" @click="closeMobile">
            <div
              class="w-10 h-10 bg-gradient-to-br from-pink-500 to-pink-600 rounded-full flex items-center justify-center"
            >
              <span class="text-white text-xl" aria-hidden="true">🍦</span>
            </div>
            <span
              class="text-2xl font-bold bg-gradient-to-r from-pink-500 to-pink-600 bg-clip-text text-transparent"
            >
              FrinStore
            </span>
          </RouterLink>

          <nav class="hidden md:flex items-center space-x-6">
            <RouterLink
              v-for="link in links"
              :key="link.path"
              :to="link.path"
              class="flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors"
              :class="
                isActive(link.path)
                  ? 'bg-pink-100 text-pink-600'
                  : 'text-gray-700 hover:bg-pink-50'
              "
            >
              <component :is="link.icon" class="w-4 h-4" />
              <span>{{ link.label }}</span>
            </RouterLink>
          </nav>

          <div class="flex items-center space-x-4">
            <RouterLink
              v-if="user?.role === 'customer'"
              to="/cart"
              class="relative"
              aria-label="Shopping cart"
            >
              <Button variant="ghost" size="icon" class="relative">
                <ShoppingCart class="w-5 h-5" />
                <span
                  v-if="cartItemCount > 0"
                  class="absolute -top-1 -right-1 min-w-[1.25rem] h-5 px-1 flex items-center justify-center rounded-full text-xs font-medium bg-pink-500 text-white"
                >
                  {{ cartItemCount }}
                </span>
              </Button>
            </RouterLink>

            <div v-if="user" class="hidden md:flex items-center space-x-2">
              <RouterLink :to="profilePath">
                <Button variant="ghost" size="icon" aria-label="Profile">
                  <User class="w-5 h-5" />
                </Button>
              </RouterLink>
              <Button
                variant="ghost"
                size="icon"
                class="text-gray-700 hover:text-pink-600"
                aria-label="Log out"
                @click="handleLogout"
              >
                <LogOut class="w-5 h-5" />
              </Button>
            </div>
            <div v-else class="hidden md:flex items-center space-x-2">
              <RouterLink to="/login">
                <Button
                  variant="outline"
                  class="border-pink-300 text-pink-600 hover:bg-pink-50"
                >
                  Login
                </Button>
              </RouterLink>
              <RouterLink to="/register">
                <Button
                  class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700"
                >
                  Sign Up
                </Button>
              </RouterLink>
            </div>

            <Button
              variant="ghost"
              size="icon"
              class="md:hidden"
              type="button"
              aria-label="Toggle menu"
              @click="mobileMenuOpen = !mobileMenuOpen"
            >
              <X v-if="mobileMenuOpen" class="w-6 h-6" />
              <Menu v-else class="w-6 h-6" />
            </Button>
          </div>
        </div>

        <div
          v-if="mobileMenuOpen"
          class="md:hidden border-t border-pink-200 py-4 space-y-2"
        >
          <RouterLink
            v-for="link in links"
            :key="link.path"
            :to="link.path"
            class="flex items-center space-x-2 px-4 py-2 rounded-lg"
            :class="
              isActive(link.path)
                ? 'bg-pink-100 text-pink-600'
                : 'text-gray-700'
            "
            @click="closeMobile"
          >
            <component :is="link.icon" class="w-5 h-5" />
            <span>{{ link.label }}</span>
          </RouterLink>
          <template v-if="user">
            <RouterLink
              v-if="user.role === 'customer'"
              to="/cart"
              class="flex items-center space-x-2 px-4 py-2 text-gray-700"
              @click="closeMobile"
            >
              <ShoppingCart class="w-5 h-5" />
              <span>Cart</span>
              <span v-if="cartItemCount > 0" class="text-pink-600 text-sm">({{ cartItemCount }})</span>
            </RouterLink>
            <RouterLink
              :to="profilePath"
              class="flex items-center space-x-2 px-4 py-2 text-gray-700"
              @click="closeMobile"
            >
              <User class="w-5 h-5" />
              <span>Profile</span>
            </RouterLink>
            <button
              type="button"
              class="flex items-center space-x-2 px-4 py-2 text-gray-700 w-full text-left"
              @click="handleLogout"
            >
              <LogOut class="w-5 h-5" />
              <span>Logout</span>
            </button>
          </template>
          <div v-else class="px-4 space-y-2">
            <RouterLink to="/login" @click="closeMobile">
              <Button variant="outline" class="w-full border-pink-300 text-pink-600">
                Login
              </Button>
            </RouterLink>
            <RouterLink to="/register" @click="closeMobile">
              <Button class="w-full bg-gradient-to-r from-pink-500 to-pink-600">
                Sign Up
              </Button>
            </RouterLink>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="bg-white border-t-2 border-pink-200 mt-12">
      <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="font-bold text-pink-600 mb-3">FrinStore</h3>
            <p class="text-gray-600 text-sm">
              Your local ice cream shop delivering happiness one scoop at a time.
            </p>
          </div>
          <div>
            <h3 class="font-bold text-pink-600 mb-3">Quick Links</h3>
            <ul class="space-y-2 text-sm text-gray-600">
              <li>
                <RouterLink to="/products" class="hover:text-pink-600">Products</RouterLink>
              </li>
              <li>
                <RouterLink to="/about" class="hover:text-pink-600">About Us</RouterLink>
              </li>
              <li>
                <RouterLink to="/contact" class="hover:text-pink-600">Contact</RouterLink>
              </li>
            </ul>
          </div>
          <div>
            <h3 class="font-bold text-pink-600 mb-3">Contact</h3>
            <p class="text-sm text-gray-600">
              Email: info@frinstore.com<br />
              Phone: (123) 456-7890
            </p>
          </div>
        </div>
        <div class="mt-8 pt-4 border-t border-pink-200 text-center text-sm text-gray-600">
          © 2026 FrinStore. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>
