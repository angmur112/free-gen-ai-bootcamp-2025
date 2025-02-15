<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Add loading state -->
      <div v-if="loading" class="flex justify-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
      </div>
      
      <!-- Add error handling -->
      <ErrorAlert v-if="error" :message="error" />
      
      <!-- Last Study Session -->
      <div v-if="lastSession" class="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-lg font-medium text-gray-900">Last Study Session</h2>
          <div class="mt-4">
            <p class="text-sm text-gray-500">
              {{ lastSession.activity_name }} - {{ formatDate(lastSession.created_at) }}
            </p>
            <div class="mt-2 flex items-center space-x-4">
              <div class="text-green-600">
                Correct: {{ lastSession.correct_count }}
              </div>
              <div class="text-red-600">
                Wrong: {{ lastSession.wrong_count }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Study Progress -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <StudyProgressCard :stats="studyProgress" />
        <QuickStatsCard :stats="quickStats" />
        <StartStudyingCard @click="navigateToStudyActivities" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import StudyProgressCard from '@/components/dashboard/StudyProgressCard.vue'
import QuickStatsCard from '@/components/dashboard/QuickStatsCard.vue'
import StartStudyingCard from '@/components/dashboard/StartStudyingCard.vue'
import { formatDate } from '@/utils/date'

const router = useRouter()
const store = useAppStore()
const loading = ref(false)
const error = ref(null)
const lastSession = ref(null)
const studyProgress = ref(null)
const quickStats = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const [sessionRes, progressRes, statsRes] = await Promise.all([
      fetch('/api/dashboard/recent-session'),
      fetch('/api/dashboard/study_progress'),
      fetch('/api/dashboard/quick_stats')
    ])
    
    // Check for response errors
    if (!sessionRes.ok || !progressRes.ok || !statsRes.ok) {
      throw new Error('Failed to fetch dashboard data')
    }
    
    lastSession.value = await sessionRes.json()
    studyProgress.value = await progressRes.json()
    quickStats.value = await statsRes.json()
  } catch (err) {
    error.value = err.message
    console.error('Failed to load dashboard data:', err)
  } finally {
    loading.value = false
  }
})

const navigateToStudyActivities = () => {
  router.push('/study-activities')
}
</script> 