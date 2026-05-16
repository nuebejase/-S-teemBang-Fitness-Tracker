<script setup lang="ts">
import { ref } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const store = useAppStore()
const category = ref('running')
const title = ref('')
const duration = ref(30)
const notes = ref('')
const saving = ref(false)

const categories = ['running', 'walking', 'cycling', 'strength', 'yoga', 'hiit', 'swimming', 'other']

async function submit() {
  saving.value = true
  try {
    await store.logWorkout({
      category: category.value,
      title: title.value || `${category.value} workout`,
      durationMinutes: duration.value,
      notes: notes.value,
    })
    toast.success('Workout logged!')
    title.value = ''
    notes.value = ''
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Failed to log workout')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-xl">
    <h1 class="text-2xl font-bold mb-2">Log workout</h1>
    <p class="text-muted-foreground mb-6">Calories are estimated from activity type and your profile weight.</p>
    <Card class="p-6 space-y-4">
      <div>
        <label class="text-sm font-medium">Category</label>
        <select v-model="category" class="mt-1 w-full px-3 py-2 rounded-lg border bg-background">
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div>
        <label class="text-sm font-medium">Title (optional)</label>
        <input v-model="title" class="mt-1 w-full px-3 py-2 rounded-lg border" placeholder="Morning run" />
      </div>
      <div>
        <label class="text-sm font-medium">Duration (minutes)</label>
        <input v-model.number="duration" type="number" min="1" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <div>
        <label class="text-sm font-medium">Notes</label>
        <textarea v-model="notes" rows="3" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <Button class="w-full" :disabled="saving" @click="submit">{{ saving ? 'Saving…' : 'Save workout' }}</Button>
    </Card>
  </div>
</template>
