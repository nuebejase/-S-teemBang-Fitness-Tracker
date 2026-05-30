import { computed, onUnmounted, ref } from 'vue'

export function useWorkoutTimer() {
  const running = ref(false)
  const elapsedSeconds = ref(0)
  let interval: ReturnType<typeof setInterval> | null = null

  const formatted = computed(() => {
    const m = Math.floor(elapsedSeconds.value / 60)
    const s = elapsedSeconds.value % 60
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  })

  const elapsedMinutes = computed(() => Math.max(1, Math.ceil(elapsedSeconds.value / 60)))

  function start() {
    if (running.value) return
    running.value = true
    interval = setInterval(() => {
      elapsedSeconds.value += 1
    }, 1000)
  }

  function stop() {
    running.value = false
    if (interval) {
      clearInterval(interval)
      interval = null
    }
  }

  function reset() {
    stop()
    elapsedSeconds.value = 0
  }

  onUnmounted(reset)

  return { running, elapsedSeconds, formatted, elapsedMinutes, start, stop, reset }
}
