<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { cn, resolveMediaUrl } from '@/lib/utils'

const props = withDefaults(
  defineProps<{
    name: string
    src?: string | null
    size?: 'sm' | 'md' | 'lg' | 'xl'
    ring?: boolean
    class?: string
  }>(),
  { size: 'md', ring: false },
)

const sizeClass = {
  sm: 'w-9 h-9 text-xs',
  md: 'w-12 h-12 text-sm',
  lg: 'w-20 h-20 text-xl',
  xl: 'w-28 h-28 text-3xl',
}[props.size]

const imgError = ref(false)

watch(
  () => props.src,
  () => {
    imgError.value = false
  },
)

const initials = computed(() =>
  props.name
    .split(' ')
    .map((w) => w[0])
    .join('')
    .slice(0, 2)
    .toUpperCase(),
)

const imageUrl = computed(() => {
  if (imgError.value) return null
  const url = resolveMediaUrl(props.src)
  if (!url) return null
  if (url.startsWith('blob:') || url.startsWith('data:')) return url
  return `${url}${url.includes('?') ? '&' : '?'}t=${encodeURIComponent(props.src ?? '')}`
})
</script>

<template>
  <div
    :class="
      cn(
        'relative rounded-full shrink-0 overflow-hidden flex items-center justify-center font-bold',
        sizeClass,
        ring && 'ring-2 ring-primary/60 ring-offset-2 ring-offset-background',
        !imageUrl && 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white',
        props.class,
      )
    "
  >
    <img
      v-if="imageUrl"
      :src="imageUrl"
      :alt="name"
      class="w-full h-full object-cover"
      @error="imgError = true"
    />
    <span v-else>{{ initials }}</span>
  </div>
</template>
