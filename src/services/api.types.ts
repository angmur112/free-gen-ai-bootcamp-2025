import type { AxiosResponse } from 'axios'
import type { 
  StudySession, 
  Word, 
  Group, 
  StudyActivity, 
  DashboardStats 
} from '@/types/models'

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  perPage: number
  totalPages: number
}

export interface ApiResponse<T> {
  data: T
  message?: string
  error?: string
}

export interface ApiError {
  message: string
  code?: string
  details?: unknown
} 