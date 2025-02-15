<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <h3 class="text-lg font-medium text-gray-900">Quick Stats</h3>
      <dl class="mt-4 grid grid-cols-2 gap-4">
        <div>
          <dt class="text-sm text-gray-500">Success Rate</dt>
          <dd class="mt-1 text-lg font-medium text-gray-900">
            {{ stats?.success_rate || 0 }}%
          </dd>
        </div>
        <div>
          <dt class="text-sm text-gray-500">Study Sessions</dt>
          <dd class="mt-1 text-lg font-medium text-gray-900">
            {{ stats?.total_sessions || 0 }}
          </dd>
        </div>
        <div>
          <dt class="text-sm text-gray-500">Active Groups</dt>
          <dd class="mt-1 text-lg font-medium text-gray-900">
            {{ stats?.active_groups || 0 }}
          </dd>
        </div>
        <div>
          <dt class="text-sm text-gray-500">Study Streak</dt>
          <dd class="mt-1 text-lg font-medium text-gray-900">
            {{ stats?.current_streak || 0 }} days
          </dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true
  }
})
</script> 