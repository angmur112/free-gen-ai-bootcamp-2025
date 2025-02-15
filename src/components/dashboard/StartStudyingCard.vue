<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <h3 class="text-lg font-medium text-gray-900">Start Studying</h3>
      <p class="mt-2 text-sm text-gray-600">
        Ready to improve your Japanese? Start a new study session now!
      </p>
      <div class="mt-4">
        <button
          @click="$emit('click')"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500"
        >
          Start New Session
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['click'])
</script> 