import { defineStore } from 'pinia'
import type { Theme } from '@/types/theme'

interface AppState {
  theme: Theme
  loading: boolean
  error: string | null
}

export const useAppStore = defineStore('app', {
  state: (): AppState => ({
    theme: 'system',
    loading: false,
    error: null
  }),
  
  actions: {
    setTheme(theme: Theme) {
      this.theme = theme
      localStorage.setItem('theme', theme)
    },
    
    setLoading(status: boolean) {
      this.loading = status
    },
    
    setError(error: string | null) {
      this.error = error
    }
  },
  
  getters: {
    isDarkMode(): boolean {
      if (this.theme === 'system') {
        return window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      return this.theme === 'dark'
    }
  }
}) 