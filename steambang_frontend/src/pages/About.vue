<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
</script>

<template>
  <div class="container mx-auto px-4 py-12 max-w-3xl">
    <h1 class="text-3xl font-bold mb-4">About (S)TeemBang</h1>
    <p class="text-muted-foreground mb-8">
      Group 4 — APAS, Labe, Tuazon, Zerrudo. A fitness tracking application aligned with our SDLC coursework:
      secure authentication, activity logging, goal setting, analytics, and reminders.
    </p>
    <div class="grid gap-4">
      <Card class="p-5">
        <h2 class="font-semibold mb-2">Included features</h2>
        <ul class="text-sm text-muted-foreground list-disc pl-5 space-y-1">
          <li>JWT-based registration and login</li>
          <li>Workout logging with calorie estimates (MET-based)</li>
          <li>Daily step sync (pedometer / manual)</li>
          <li>Daily, weekly, and monthly goals with progress</li>
          <li>Dashboard analytics and trend charts</li>
          <li>Profile management and notifications</li>
        </ul>
      </Card>
      <Card class="p-5">
        <h2 class="font-semibold mb-2">Tech stack</h2>
        <p class="text-sm text-muted-foreground">Vue 3 + Vite + Pinia + Tailwind · FastAPI + SQLAlchemy + SQLite</p>
      </Card>
    </div>
  </div>
</template>
