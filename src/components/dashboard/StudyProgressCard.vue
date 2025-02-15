<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <h3 class="text-lg font-medium text-gray-900">Study Progress</h3>
      <div class="mt-4">
        <div class="flex justify-between items-center">
          <span class="text-sm text-gray-500">Words Studied</span>
          <span class="text-sm font-medium text-gray-900">
            {{ stats?.total_words_studied || 0 }}/{{ stats?.total_vocabulary || 0 }}
          </span>
        </div>
        <div class="mt-4">
          <div class="relative pt-1">
            <div class="overflow-hidden h-2 text-xs flex rounded bg-brand-100">
              <div
                :style="`width: ${progressPercentage}%`"
                class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-brand-600"
              ></div>
            </div>
          </div>
        </div>
        <div class="mt-2 text-sm text-gray-600">
          Mastery: {{ stats?.mastered_words || 0 }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    required: true
  }
})

const progressPercentage = computed(() => {
  if (!props.stats?.total_vocabulary) return 0
  return (props.stats.total_words_studied / props.stats.total_vocabulary) * 100
})
</script> 