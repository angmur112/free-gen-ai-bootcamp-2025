export const config = {
  apiUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  environment: import.meta.env.MODE,
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD
} 