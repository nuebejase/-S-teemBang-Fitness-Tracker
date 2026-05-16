import { STORAGE_KEYS } from '@/constants/storage'
import type { CartItem, Order, OrderStatus, Product, User } from '@/types/domain'

/** Empty in dev when `VITE_API_URL` is unset → browser calls same origin and Vite proxies `/api` → :8000 */
function resolveApiBase(): string {
  const raw = import.meta.env.VITE_API_URL as string | undefined
  if (typeof raw === 'string' && raw.trim() !== '') {
    return raw.replace(/\/$/, '')
  }
  if (import.meta.env.DEV) {
    return ''
  }
  return 'http://localhost:8000'
}

const API_BASE = resolveApiBase()

type ApiDetail = string | { msg?: string }[] | Record<string, unknown>

function formatError(res: Response, data: unknown): string {
  const d = data as { detail?: ApiDetail }
  const detail = d?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((x) => (typeof x === 'object' && x && 'msg' in x ? String((x as { msg: string }).msg) : JSON.stringify(x))).join(', ')
  }
  if (detail && typeof detail === 'object') return JSON.stringify(detail)
  return res.statusText || 'Request failed'
}

export async function apiJson<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path.startsWith('/') ? path : `/${path}`}`
  const headers = new Headers(init?.headers)
  const hasBody = init?.body !== undefined && init?.body !== null
  if (hasBody && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  const token = localStorage.getItem(STORAGE_KEYS.accessToken)
  if (token) headers.set('Authorization', `Bearer ${token}`)

  let res: Response
  try {
    res = await fetch(url, { ...init, headers })
  } catch (e) {
    const hint =
      import.meta.env.DEV && API_BASE === ''
        ? ' Start the API (see terminal): cd frinstore_backend && .venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000'
        : ` (${url})`
    throw new Error(
      e instanceof TypeError ? `Cannot reach FrinStore API.${hint}` : String(e),
    )
  }
  const text = await res.text()
  const data = text ? (JSON.parse(text) as unknown) : null

  if (!res.ok) {
    throw new Error(formatError(res, data))
  }

  if (res.status === 204) {
    return undefined as T
  }

  return data as T
}

/* --- API shapes (snake_case from server) --- */

interface ApiUser {
  id: string
  name: string
  email: string
  role: 'customer' | 'admin'
}

interface ApiProduct {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  flavor: string
  stock: number
}

interface ApiCartItem extends ApiProduct {
  quantity: number
}

interface ApiOrder {
  id: string
  customer_name: string
  customer_email: string
  customer_phone: string
  address: string
  payment_method: string
  status: OrderStatus
  date: string
  total: number
  items: ApiCartItem[]
}

function mapProduct(p: ApiProduct): Product {
  return {
    id: p.id,
    name: p.name,
    description: p.description,
    price: p.price,
    image: p.image,
    category: p.category,
    flavor: p.flavor,
    stock: p.stock,
  }
}

function mapCartItem(i: ApiCartItem): CartItem {
  return {
    ...mapProduct(i),
    quantity: i.quantity,
  }
}

function mapOrder(o: ApiOrder): Order {
  return {
    id: o.id,
    customerName: o.customer_name,
    customerEmail: o.customer_email,
    customerPhone: o.customer_phone,
    address: o.address,
    paymentMethod: o.payment_method,
    status: o.status,
    date: o.date,
    total: o.total,
    items: o.items.map(mapCartItem),
  }
}

export async function fetchProductsApi(): Promise<Product[]> {
  const rows = await apiJson<ApiProduct[]>('/api/products')
  return rows.map(mapProduct)
}

export async function fetchMeApi(): Promise<User> {
  const u = await apiJson<ApiUser>('/api/auth/me')
  return { id: u.id, name: u.name, email: u.email, role: u.role }
}

export async function loginApi(email: string, password: string): Promise<string> {
  const res = await apiJson<{ access_token: string }>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  return res.access_token
}

export async function registerApi(name: string, email: string, password: string): Promise<string> {
  const res = await apiJson<{ access_token: string }>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
  return res.access_token
}

export async function createProductApi(payload: Omit<Product, 'id'>): Promise<Product> {
  const p = await apiJson<ApiProduct>('/api/products', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  return mapProduct(p)
}

export async function updateProductApi(
  productId: string,
  payload: Partial<Omit<Product, 'id'>>,
): Promise<Product> {
  const p = await apiJson<ApiProduct>(`/api/products/${encodeURIComponent(productId)}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
  return mapProduct(p)
}

export async function deleteProductApi(productId: string): Promise<void> {
  await apiJson<void>(`/api/products/${encodeURIComponent(productId)}`, {
    method: 'DELETE',
  })
}

export interface CreateOrderBody {
  items: { product_id: string; quantity: number }[]
  customer_name: string
  customer_email: string
  customer_phone: string
  address: string
  payment_method: string
  delivery_fee: number
}

export async function createOrderApi(body: CreateOrderBody): Promise<Order> {
  const o = await apiJson<ApiOrder>('/api/orders', {
    method: 'POST',
    body: JSON.stringify(body),
  })
  return mapOrder(o)
}

export async function fetchMyOrdersApi(): Promise<Order[]> {
  const rows = await apiJson<ApiOrder[]>('/api/orders/me')
  return rows.map(mapOrder)
}

export async function fetchAllOrdersApi(): Promise<Order[]> {
  const rows = await apiJson<ApiOrder[]>('/api/orders')
  return rows.map(mapOrder)
}

export async function updateOrderStatusApi(orderId: string, status: OrderStatus): Promise<Order> {
  const o = await apiJson<ApiOrder>(`/api/orders/${encodeURIComponent(orderId)}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  })
  return mapOrder(o)
}

export function getApiBase(): string {
  return API_BASE
}
