<script setup lang="ts">
import { computed } from 'vue'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white hover:from-emerald-400 hover:to-teal-400 btn-glow',
        secondary: 'bg-secondary/90 text-secondary-foreground hover:bg-secondary',
        outline: 'border border-white/15 bg-white/[0.03] hover:bg-white/[0.07] hover:border-white/25',
        ghost: 'hover:bg-white/[0.06]',
        destructive: 'bg-red-500/90 text-white hover:bg-red-500',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3',
        lg: 'h-11 px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
)

interface Props extends /* @vue-ignore */ VariantProps<typeof buttonVariants> {
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), { variant: 'default', size: 'default' })
const className = computed(() => cn(buttonVariants({ variant: props.variant, size: props.size })))
</script>

<template>
  <button :class="className" :disabled="disabled">
    <slot />
  </button>
</template>
