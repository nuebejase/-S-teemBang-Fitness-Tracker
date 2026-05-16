import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import {
  createOrderApi,
  createProductApi,
  deleteProductApi,
  fetchAllOrdersApi,
  fetchMeApi,
  fetchMyOrdersApi,
  fetchProductsApi,
  loginApi,
  registerApi,
  updateOrderStatusApi,
  updateProductApi,
} from '@/lib/api'
import { STORAGE_KEYS } from '@/constants/storage'
import type { CartItem, NewOrderPayload, Order, OrderStatus, Product, User } from '@/types/domain'

export type { CartItem, Order, Product, User } from '@/types/domain'

function readJson<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) return fallback
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

export const useAppStore = defineStore('app', () => {
  const user = ref<User | null>(null)
  const cart = ref<CartItem[]>([])
  const products = ref<Product[]>([])
  const orders = ref<Order[]>([])
  const productsLoading = ref(false)
  const ordersLoading = ref(false)
  /** Set when catalog cannot be loaded (e.g. API down). */
  const bootstrapError = ref<string | null>(null)

  const cartTotal = computed(() =>
    cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
  )

  const cartItemCount = computed(() =>
    cart.value.reduce((sum, item) => sum + item.quantity, 0),
  )

  function persistCart() {
    localStorage.setItem(STORAGE_KEYS.cart, JSON.stringify(cart.value))
  }

  function loadCartFromStorage() {
    cart.value = readJson(STORAGE_KEYS.cart, [])
  }

  watch(cart, persistCart, { deep: true })

  function reconcileCartWithCatalog() {
    const ps = products.value
    cart.value = cart.value.flatMap((item) => {
      const p = ps.find((x) => x.id === item.id)
      if (!p || p.stock <= 0) return []
      const qty = Math.min(item.quantity, p.stock)
      return [{ ...p, quantity: qty }]
    })
  }

  async function fetchProducts() {
    productsLoading.value = true
    bootstrapError.value = null
    try {
      products.value = await fetchProductsApi()
      reconcileCartWithCatalog()
    } catch (e) {
      bootstrapError.value = e instanceof Error ? e.message : 'Could not load catalog'
      products.value = []
    } finally {
      productsLoading.value = false
    }
  }

  async function refreshOrders() {
    if (!user.value) {
      orders.value = []
      return
    }
    ordersLoading.value = true
    try {
      if (user.value.role === 'admin') {
        orders.value = await fetchAllOrdersApi()
      } else {
        orders.value = await fetchMyOrdersApi()
      }
    } catch {
      orders.value = []
    } finally {
      ordersLoading.value = false
    }
  }

  async function initializeApp() {
    loadCartFromStorage()
    await fetchProducts()
    const token = localStorage.getItem(STORAGE_KEYS.accessToken)
    if (!token) {
      user.value = null
      orders.value = []
      return
    }
    try {
      user.value = await fetchMeApi()
      await refreshOrders()
    } catch {
      localStorage.removeItem(STORAGE_KEYS.accessToken)
      user.value = null
      orders.value = []
    }
  }

  async function login(email: string, password: string): Promise<void> {
    const token = await loginApi(email, password)
    localStorage.setItem(STORAGE_KEYS.accessToken, token)
    user.value = await fetchMeApi()
    await refreshOrders()
  }

  async function register(name: string, email: string, password: string): Promise<void> {
    const token = await registerApi(name, email, password)
    localStorage.setItem(STORAGE_KEYS.accessToken, token)
    user.value = await fetchMeApi()
    await refreshOrders()
  }

  function logout() {
    user.value = null
    orders.value = []
    localStorage.removeItem(STORAGE_KEYS.accessToken)
  }

  /** Returns true if quantity increased or line was added; false if out of stock or already at max. */
  const addToCart = (product: Product): boolean => {
    if (product.stock <= 0) return false
    const existingItem = cart.value.find((item) => item.id === product.id)
    if (existingItem) {
      if (existingItem.quantity >= product.stock) return false
      existingItem.quantity += 1
    } else {
      cart.value.push({ ...product, quantity: 1 })
    }
    return true
  }

  const removeFromCart = (productId: string) => {
    cart.value = cart.value.filter((item) => item.id !== productId)
  }

  const updateCartQuantity = (productId: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(productId)
      return
    }
    const item = cart.value.find((i) => i.id === productId)
    if (item) {
      item.quantity = Math.min(quantity, item.stock)
    }
  }

  const clearCart = () => {
    cart.value = []
  }

  const createOrder = async (orderData: NewOrderPayload): Promise<Order> => {
    const order = await createOrderApi({
      items: cart.value.map((i) => ({ product_id: i.id, quantity: i.quantity })),
      customer_name: orderData.customerName,
      customer_email: orderData.customerEmail,
      customer_phone: orderData.customerPhone,
      address: orderData.address,
      payment_method: orderData.paymentMethod,
      delivery_fee: 50,
    })
    clearCart()
    await fetchProducts()
    await refreshOrders()
    return order
  }

  const updateOrderStatus = async (orderId: string, status: OrderStatus) => {
    const updated = await updateOrderStatusApi(orderId, status)
    const idx = orders.value.findIndex((o) => o.id === orderId)
    if (idx !== -1) {
      orders.value[idx] = updated
    } else {
      await refreshOrders()
    }
  }

  const addProduct = async (product: Omit<Product, 'id'>) => {
    const created = await createProductApi(product)
    products.value.push(created)
  }

  const updateProduct = async (productId: string, updatedProduct: Partial<Product>) => {
    const updated = await updateProductApi(productId, updatedProduct)
    const idx = products.value.findIndex((p) => p.id === productId)
    if (idx !== -1) {
      products.value[idx] = updated
    }
    await fetchProducts()
  }

  const deleteProduct = async (productId: string) => {
    await deleteProductApi(productId)
    products.value = products.value.filter((p) => p.id !== productId)
  }

  return {
    user,
    cart,
    products,
    orders,
    productsLoading,
    ordersLoading,
    bootstrapError,
    cartTotal,
    cartItemCount,
    initializeApp,
    fetchProducts,
    refreshOrders,
    login,
    register,
    logout,
    addToCart,
    removeFromCart,
    updateCartQuantity,
    clearCart,
    createOrder,
    updateOrderStatus,
    addProduct,
    updateProduct,
    deleteProduct,
  }
})
