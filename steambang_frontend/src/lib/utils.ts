import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(n: number): string {
  return new Intl.NumberFormat().format(Math.round(n))
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

function resolveApiBase(): string {
  const raw = import.meta.env.VITE_API_URL as string | undefined
  if (typeof raw === 'string' && raw.trim() !== '') return raw.replace(/\/$/, '')
  if (import.meta.env.DEV) return ''
  return 'http://localhost:8000'
}

export function resolveMediaUrl(path: string | null | undefined): string | null {
  if (!path) return null
  if (path.startsWith('http') || path.startsWith('data:') || path.startsWith('blob:')) return path
  const envBase = resolveApiBase()
  // Uploads are served by FastAPI — point directly at the backend in dev
  const base = envBase || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : 'http://localhost:8000')
  return `${base}${path.startsWith('/') ? path : `/${path}`}`
}

export function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1)
}
