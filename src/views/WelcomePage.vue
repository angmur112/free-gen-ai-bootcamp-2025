<template>
  <div class="min-h-screen bg-gradient-to-br from-brand-50 to-brand-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center">
        <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Welcome to Language Portal
        </h1>
        <p class="mt-6 text-lg leading-8 text-gray-600">
          Your personal Japanese language learning companion
        </p>
        <div class="mt-10 flex items-center justify-center gap-x-6">
          <RouterLink
            to="/dashboard"
            class="rounded-md bg-brand-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-brand-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600"
          >
            Get Started
          </RouterLink>
          <a href="#features" class="text-sm font-semibold leading-6 text-gray-900">
            Learn more <span aria-hidden="true">→</span>
          </a>
        </div>
      </div>

      <div id="features" class="mt-32">
        <div class="grid grid-cols-1 gap-y-16 gap-x-8 sm:grid-cols-2 lg:grid-cols-3">
          <div class="text-center">
            <div class="flex justify-center">
              <BookOpenIcon class="h-10 w-10 text-brand-600" />
            </div>
            <h3 class="mt-6 text-base font-semibold leading-7 text-gray-900">
              Extensive Vocabulary
            </h3>
            <p class="mt-2 text-sm text-gray-600">
              Access a comprehensive database of Japanese words and phrases
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { BookOpenIcon } from '@heroicons/vue/24/outline'
import { RouterLink } from 'vue-router'
</script> 