import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const dashboardService = {
  getRecentSession: () => api.get('/dashboard/recent-session'),
  getStudyProgress: () => api.get('/dashboard/study_progress'),
  getQuickStats: () => api.get('/dashboard/quick_stats')
}

export const studySessionService = {
  create: (data) => api.post('/study-sessions', data),
  submitReview: (sessionId, data) => api.post(`/study-sessions/${sessionId}/review`, data)
}

export default api 