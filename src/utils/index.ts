export function formatDate(dateString: string): string {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

export function calculateProgress(current: number, total: number): number {
  if (!total) return 0
  return Math.round((current / total) * 100)
} 