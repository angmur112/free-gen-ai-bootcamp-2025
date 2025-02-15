import axios, { type AxiosInstance } from 'axios'
import type { 
  ApiResponse, 
  PaginatedResponse 
} from './api.types'
import type { 
  StudySession, 
  DashboardStats, 
  Word, 
  Group 
} from '@/types/models'
import { config } from '@/config'

const api: AxiosInstance = axios.create({
  baseURL: config.apiUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const dashboardService = {
  getRecentSession: () => 
    api.get<ApiResponse<StudySession>>('/dashboard/recent-session'),
    
  getStudyProgress: () => 
    api.get<ApiResponse<DashboardStats>>('/dashboard/study_progress'),
    
  getQuickStats: () => 
    api.get<ApiResponse<DashboardStats>>('/dashboard/quick_stats')
}

export const studySessionService = {
  create: (data: { groupId: number; activityId: number }) => 
    api.post<ApiResponse<{ id: number }>>('/study-sessions', data),
    
  submitReview: (sessionId: number, data: { wordId: number; correct: boolean }) => 
    api.post<ApiResponse<void>>(`/study-sessions/${sessionId}/review`, data),
    
  getList: (page: number = 1, perPage: number = 10) => 
    api.get<PaginatedResponse<StudySession>>('/study-sessions', {
      params: { page, perPage }
    })
}

// Add more services...

export default api 