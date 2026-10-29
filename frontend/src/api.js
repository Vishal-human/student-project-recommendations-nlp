const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const token = localStorage.getItem('token')
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`${API_URL}${path}`, { ...options, headers })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.detail || 'Request failed')
  }
  return data
}

export const signup = (payload) => request('/auth/signup', { method: 'POST', body: JSON.stringify(payload) })
export const login = (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) })
export const getMe = () => request('/auth/me')
export const forgotPassword = (payload) =>
  request('/auth/forgot-password', { method: 'POST', body: JSON.stringify(payload) })
export const resetPassword = (payload) =>
  request('/auth/reset-password', { method: 'POST', body: JSON.stringify(payload) })
export const getStudentDashboard = () => request('/dashboard/student')
export const getSupervisorDashboard = () => request('/dashboard/supervisor')
export const getTeacherDashboard = () => request('/dashboard/teacher')
export const getStudents = () => request('/teacher/students')
export const getDomains = () => request('/topics/domains')
export const getRecommendations = (payload) =>
  request('/topics/recommend', { method: 'POST', body: JSON.stringify(payload) })
export const generateTopics = (payload) =>
  request('/topics/generate', { method: 'POST', body: JSON.stringify(payload) })
export const checkDuplicates = (topics) =>
  request('/supervisor/check-duplicates', { method: 'POST', body: JSON.stringify(topics) })

// Proposal endpoints
export const submitProposal = (payload) =>
  request('/proposals/submit', { method: 'POST', body: JSON.stringify(payload) })
export const getMyProposals = () => request('/proposals/mine')
export const getPendingProposals = () => request('/proposals/pending')
export const getAllProposals = () => request('/proposals/all')
export const approveProposal = (id, notes = '') =>
  request(`/proposals/${id}/approve`, { method: 'POST', body: JSON.stringify({ notes }) })
export const rejectProposal = (id, notes = '') =>
  request(`/proposals/${id}/reject`, { method: 'POST', body: JSON.stringify({ notes }) })
