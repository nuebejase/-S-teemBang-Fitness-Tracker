import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { toast } from 'vue-sonner'
import 'vue-sonner/style.css'
import './styles/globals.css'
import App from './App.vue'
import router from './router'
import { useAppStore } from '@/stores/appStore'

async function bootstrap() {
  const app = createApp(App)
  app.use(createPinia())
  const store = useAppStore()
  await store.initializeApp()
  app.use(router)
  app.mount('#app')
  if (store.bootstrapError) toast.error(store.bootstrapError)
}

void bootstrap()
