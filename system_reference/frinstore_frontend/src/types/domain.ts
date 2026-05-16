export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface Product {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  flavor: string
  stock: number
}

export interface CartItem extends Product {
  quantity: number
}

export interface Order {
  id: string
  items: CartItem[]
  total: number
  status: OrderStatus
  date: string
  customerName: string
  customerEmail: string
  customerPhone: string
  address: string
  paymentMethod: string
}

export interface User {
  id: string
  name: string
  email: string
  role: 'customer' | 'admin'
}

export type NewOrderPayload = Omit<Order, 'id' | 'date' | 'items' | 'total'>
