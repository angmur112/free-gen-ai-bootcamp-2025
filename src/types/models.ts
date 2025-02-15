export interface StudySession {
  id: number
  groupId: number
  groupName: string
  activityId: number
  activityName: string
  startTime: string
  endTime: string
  reviewItemsCount: number
  correctCount?: number
  wrongCount?: number
}

export interface Word {
  id: number
  kanji: string
  romaji: string
  english: string
  correctCount: number
  wrongCount: number
  groups?: Group[]
}

export interface Group {
  id: number
  name: string
  wordsCount: number
}

export interface StudyActivity {
  id: number
  name: string
  url: string
  previewUrl: string
  description?: string
}

export interface DashboardStats {
  totalVocabulary: number
  totalWordsStudied: number
  masteredWords: number
  successRate: number
  totalSessions: number
  activeGroups: number
  currentStreak: number
} 