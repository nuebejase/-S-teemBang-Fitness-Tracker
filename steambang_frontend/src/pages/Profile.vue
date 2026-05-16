<script setup lang="ts">
import { ref, watch } from 'vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { toast } from 'vue-sonner'

const store = useAppStore()
const height = ref<number | ''>('')
const weight = ref<number | ''>('')
const age = ref<number | ''>('')
const level = ref('beginner')
const stepTarget = ref(8000)

watch(
  () => store.profile,
  (p) => {
    if (!p) return
    height.value = p.heightCm ?? ''
    weight.value = p.weightKg ?? ''
    age.value = p.age ?? ''
    level.value = p.fitnessLevel
    stepTarget.value = p.dailyStepTarget
  },
  { immediate: true },
)

async function save() {
  try {
    await store.saveProfile({
      heightCm: height.value === '' ? null : Number(height.value),
      weightKg: weight.value === '' ? null : Number(weight.value),
      age: age.value === '' ? null : Number(age.value),
      fitnessLevel: level.value,
      dailyStepTarget: stepTarget.value,
    })
    toast.success('Profile updated')
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Save failed')
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-lg">
    <h1 class="text-2xl font-bold mb-2">Profile</h1>
    <p v-if="store.user" class="text-muted-foreground mb-6">{{ store.user.name }} · {{ store.user.email }}</p>
    <Card class="p-6 space-y-4">
      <div>
        <label class="text-sm font-medium">Height (cm)</label>
        <input v-model.number="height" type="number" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <div>
        <label class="text-sm font-medium">Weight (kg)</label>
        <input v-model.number="weight" type="number" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <div>
        <label class="text-sm font-medium">Age</label>
        <input v-model.number="age" type="number" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <div>
        <label class="text-sm font-medium">Fitness level</label>
        <select v-model="level" class="mt-1 w-full px-3 py-2 rounded-lg border">
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <div>
        <label class="text-sm font-medium">Daily step target</label>
        <input v-model.number="stepTarget" type="number" min="1000" class="mt-1 w-full px-3 py-2 rounded-lg border" />
      </div>
      <Button class="w-full" @click="save">Save profile</Button>
    </Card>
  </div>
</template>
