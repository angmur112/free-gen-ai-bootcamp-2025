import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    theme: 'system',
    loading: false,
    error: null,
    user: null,
  }),
  
  actions: {
    setTheme(theme) {
      this.theme = theme
      localStorage.setItem('theme', theme)
    },
    
    setLoading(status) {
      this.loading = status
    },
    
    setError(error) {
      this.error = error
    }
  }
}) 