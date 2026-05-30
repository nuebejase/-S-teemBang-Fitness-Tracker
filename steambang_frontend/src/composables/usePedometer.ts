import { onUnmounted, ref } from 'vue'

/** Simulated pedometer for desktop/demo — adds steps automatically while running. */
export function usePedometer() {
  const sessionSteps = ref(0)
  const tracking = ref(false)
  const supported = ref(true)
  const isSimulated = ref(true)
  const error = ref<string | null>(null)

  let simTimer: ReturnType<typeof setInterval> | null = null

  function startSimulation() {
    stopSimulation()
    isSimulated.value = true
    simTimer = setInterval(() => {
      sessionSteps.value += Math.floor(Math.random() * 5) + 3
    }, 700)
    tracking.value = true
    return true
  }

  function stopSimulation() {
    if (simTimer) {
      clearInterval(simTimer)
      simTimer = null
    }
  }

  async function start() {
    error.value = null
    return startSimulation()
  }

  function stop() {
    stopSimulation()
    tracking.value = false
  }

  function reset() {
    sessionSteps.value = 0
  }

  onUnmounted(stop)

  return { sessionSteps, tracking, supported, isSimulated, error, start, stop, reset }
}
