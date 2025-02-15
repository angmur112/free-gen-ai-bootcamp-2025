const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3000/api';

export const api = {
  // Dashboard
  getLastStudySession: () => fetch(`${API_BASE_URL}/dashboard/last_study_session`).then(res => res.json()),
  getStudyProgress: () => fetch(`${API_BASE_URL}/dashboard/study_progress`).then(res => res.json()),
  getQuickStats: () => fetch(`${API_BASE_URL}/dashboard/quick_stats`).then(res => res.json()),

  // Study Activities
  getStudyActivities: () => fetch(`${API_BASE_URL}/study_activities`).then(res => res.json()),
  getStudyActivity: (id) => fetch(`${API_BASE_URL}/study_activities/${id}`).then(res => res.json()),
  getStudyActivitySessions: (id) => fetch(`${API_BASE_URL}/study_activities/${id}/study_sessions`).then(res => res.json()),
  createStudyActivity: (data) => fetch(`${API_BASE_URL}/study_activities`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json()),

  // Words
  getWords: (page) => fetch(`${API_BASE_URL}/words?page=${page}`).then(res => res.json()),
  getWord: (id) => fetch(`${API_BASE_URL}/words/${id}`).then(res => res.json()),

  // Groups
  getGroups: () => fetch(`${API_BASE_URL}/groups`).then(res => res.json()),
  getGroup: (id) => fetch(`${API_BASE_URL}/groups/${id}`).then(res => res.json()),
  getGroupWords: (id, page) => fetch(`${API_BASE_URL}/groups/${id}/words?page=${page}`).then(res => res.json()),
  getGroupStudySessions: (id) => fetch(`${API_BASE_URL}/groups/${id}/study_sessions`).then(res => res.json()),

  // Study Sessions
  getStudySessions: () => fetch(`${API_BASE_URL}/study_sessions`).then(res => res.json()),
  getStudySession: (id) => fetch(`${API_BASE_URL}/study_sessions/${id}`).then(res => res.json()),
  getStudySessionWords: (id) => fetch(`${API_BASE_URL}/study_sessions/${id}/words`).then(res => res.json()),

  // Settings
  resetHistory: () => fetch(`${API_BASE_URL}/reset_history`, { method: 'POST' }).then(res => res.json()),
  fullReset: () => fetch(`${API_BASE_URL}/full_reset`, { method: 'POST' }).then(res => res.json()),
};

export default api; 