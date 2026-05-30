<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Avatar from '@/components/Avatar.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { useAppStore } from '@/stores/appStore'
import { Camera, Edit3, Footprints, Flame, Dumbbell, Ruler, Scale, User, Zap } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const store = useAppStore()
const editing = ref(false)
const saving = ref(false)
const uploading = ref(false)
const previewUrl = ref<string | null>(null)

const height = ref<number | ''>('')
const weight = ref<number | ''>('')
const age = ref<number | ''>('')
const level = ref('beginner')
const stepTarget = ref(8000)
const calorieTarget = ref(500)
const workoutTarget = ref(1)

const profile = computed(() => store.profile)
const showView = computed(() => profile.value?.isComplete && !editing.value)

watch(
  () => store.profile,
  (p) => {
    if (!p) return
    height.value = p.heightCm ?? ''
    weight.value = p.weightKg ?? ''
    age.value = p.age ?? ''
    level.value = p.fitnessLevel
    stepTarget.value = p.dailyStepTarget
    calorieTarget.value = p.dailyCalorieTarget
    workoutTarget.value = p.dailyWorkoutTarget
    if (!p.isComplete) editing.value = true
  },
  { immediate: true },
)

function loadFormFromProfile() {
  const p = store.profile
  if (!p) return
  height.value = p.heightCm ?? ''
  weight.value = p.weightKg ?? ''
  age.value = p.age ?? ''
  level.value = p.fitnessLevel
  stepTarget.value = p.dailyStepTarget
  calorieTarget.value = p.dailyCalorieTarget
  workoutTarget.value = p.dailyWorkoutTarget
}

function startEdit() {
  loadFormFromProfile()
  editing.value = true
}

function cancelEdit() {
  if (profile.value?.isComplete) {
    loadFormFromProfile()
    editing.value = false
    previewUrl.value = null
  }
}

async function onPhotoPick(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    toast.error('Photo must be under 2 MB')
    return
  }
  previewUrl.value = URL.createObjectURL(file)
  uploading.value = true
  try {
    await store.uploadAvatar(file)
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
    toast.success('Profile photo updated')
  } catch (err) {
    toast.error(err instanceof Error ? err.message : 'Upload failed')
    previewUrl.value = null
  } finally {
    uploading.value = false
    input.value = ''
  }
}

async function save() {
  saving.value = true
  try {
    await store.saveProfile({
      heightCm: height.value === '' ? null : Number(height.value),
      weightKg: weight.value === '' ? null : Number(weight.value),
      age: age.value === '' ? null : Number(age.value),
      fitnessLevel: level.value,
      dailyStepTarget: stepTarget.value,
      dailyCalorieTarget: calorieTarget.value,
      dailyWorkoutTarget: workoutTarget.value,
    })
    toast.success('Profile saved')
    editing.value = false
    previewUrl.value = null
  } catch (e) {
    toast.error(e instanceof Error ? e.message : 'Save failed')
  } finally {
    saving.value = false
  }
}

const avatarSrc = computed(() => previewUrl.value ?? profile.value?.avatarUrl)
</script>

<template>
  <div class="container mx-auto px-4 py-8 max-w-lg">
    <!-- View mode -->
    <div v-if="showView" class="space-y-6">
      <div class="text-center">
        <div class="relative inline-block mb-4">
          <Avatar :name="store.user?.name ?? 'User'" :src="avatarSrc" size="xl" ring />
        </div>
        <h1 class="text-2xl font-bold tracking-tight">{{ store.user?.name }}</h1>
        <p class="text-muted-foreground text-sm mt-1">{{ store.user?.email }}</p>
        <Button variant="outline" size="sm" class="mt-4" @click="startEdit">
          <Edit3 class="w-4 h-4 mr-2" /> Edit profile
        </Button>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <Card class="p-4 text-center">
          <Ruler class="w-5 h-5 mx-auto text-emerald-400 mb-2" />
          <p class="premium-label">Height</p>
          <p class="text-xl font-bold mt-1">{{ profile?.heightCm }} cm</p>
        </Card>
        <Card class="p-4 text-center">
          <Scale class="w-5 h-5 mx-auto text-cyan-400 mb-2" />
          <p class="premium-label">Weight</p>
          <p class="text-xl font-bold mt-1">{{ profile?.weightKg }} kg</p>
        </Card>
        <Card class="p-4 text-center">
          <User class="w-5 h-5 mx-auto text-violet-400 mb-2" />
          <p class="premium-label">Age</p>
          <p class="text-xl font-bold mt-1">{{ profile?.age }} yrs</p>
        </Card>
        <Card class="p-4 text-center">
          <Zap class="w-5 h-5 mx-auto text-amber-400 mb-2" />
          <p class="premium-label">Level</p>
          <p class="text-xl font-bold mt-1 capitalize">{{ profile?.fitnessLevel }}</p>
        </Card>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card class="p-4 flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-500/15 flex items-center justify-center shrink-0">
            <Footprints class="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <p class="premium-label">Daily steps</p>
            <p class="text-xl font-bold">{{ profile?.dailyStepTarget?.toLocaleString() }}</p>
          </div>
        </Card>
        <Card class="p-4 flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-orange-500/15 flex items-center justify-center shrink-0">
            <Flame class="w-5 h-5 text-orange-400" />
          </div>
          <div>
            <p class="premium-label">Daily calories</p>
            <p class="text-xl font-bold">{{ profile?.dailyCalorieTarget }} kcal</p>
          </div>
        </Card>
        <Card class="p-4 flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-500/15 flex items-center justify-center shrink-0">
            <Dumbbell class="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <p class="premium-label">Daily workouts</p>
            <p class="text-xl font-bold">{{ profile?.dailyWorkoutTarget }} session{{ (profile?.dailyWorkoutTarget ?? 0) > 1 ? 's' : '' }}</p>
          </div>
        </Card>
      </div>
    </div>

    <!-- Edit / setup mode -->
    <div v-else class="space-y-6">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">
          {{ profile?.isComplete ? 'Edit profile' : 'Set up your profile' }}
        </h1>
        <p class="text-muted-foreground text-sm mt-1">
          {{ profile?.isComplete ? 'Update your details and photo.' : 'Complete your profile to unlock personalized tracking.' }}
        </p>
      </div>

      <div class="flex flex-col items-center gap-3">
        <div class="relative">
          <Avatar :name="store.user?.name ?? 'User'" :src="avatarSrc" size="xl" ring />
          <label
            class="absolute -bottom-1 -right-1 w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center cursor-pointer shadow-lg hover:scale-105 transition-transform"
            :class="uploading ? 'opacity-50 pointer-events-none' : ''"
          >
            <Camera class="w-5 h-5 text-white" />
            <input type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="hidden" @change="onPhotoPick" />
          </label>
        </div>
        <p class="text-xs text-muted-foreground">Tap camera to add profile photo</p>
      </div>

      <Card class="p-6 space-y-5">
        <div>
          <label class="premium-label">Height (cm)</label>
          <input v-model.number="height" type="number" class="premium-input mt-2" placeholder="170" />
        </div>
        <div>
          <label class="premium-label">Weight (kg)</label>
          <input v-model.number="weight" type="number" class="premium-input mt-2" placeholder="68" />
        </div>
        <div>
          <label class="premium-label">Age</label>
          <input v-model.number="age" type="number" class="premium-input mt-2" placeholder="25" />
        </div>
        <div>
          <label class="premium-label">Fitness level</label>
          <select v-model="level" class="premium-input mt-2">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label class="premium-label">Daily step target</label>
          <input v-model.number="stepTarget" type="number" min="1000" class="premium-input mt-2" />
        </div>
        <div>
          <label class="premium-label">Daily calorie target (kcal)</label>
          <input v-model.number="calorieTarget" type="number" min="50" class="premium-input mt-2" />
        </div>
        <div>
          <label class="premium-label">Daily workout target (sessions)</label>
          <input v-model.number="workoutTarget" type="number" min="1" max="10" class="premium-input mt-2" />
        </div>
        <div class="flex gap-3 pt-2">
          <Button v-if="profile?.isComplete" variant="outline" class="flex-1" @click="cancelEdit">Cancel</Button>
          <Button class="flex-1" :disabled="saving" @click="save">
            {{ saving ? 'Saving…' : 'Save profile' }}
          </Button>
        </div>
      </Card>
    </div>
  </div>
</template>
