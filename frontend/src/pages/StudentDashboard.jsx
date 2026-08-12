import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import { getDomains, getMe, getStudentDashboard } from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function StudentDashboard() {
  const { auth } = useAuth()
  const [dashboard, setDashboard] = useState(null)
  const [me, setMe] = useState(null)
  const [domains, setDomains] = useState(null)

  useEffect(() => {
    getStudentDashboard().then(setDashboard).catch(() => {})
    getMe().then(setMe).catch(() => {})
    getDomains().then(setDomains).catch(() => {})
  }, [])

  return (
    <div>
      <Navbar />
      <div className="page">
        <h1>Welcome, {auth?.name}</h1>
        <p className="muted">{dashboard?.next_step}</p>

        <div className="stat-grid">
          <div className="stat-card">
            <span className="stat-label">Account</span>
            <span className="stat-value">Active</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Project Domains</span>
            <span className="stat-value">{domains?.domains?.length ?? '—'}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Topics in Database</span>
            <span className="stat-value">{domains?.total_topics ?? '—'}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Joined</span>
            <span className="stat-value">
              {me ? new Date(me.created_at).toLocaleDateString() : '—'}
            </span>
          </div>
        </div>

        <div className="card">
          <h2>Recommended Topics</h2>
          <p className="muted">
            The NLP-based topic recommender (matching your interests to project ideas using
            sentence embeddings) is a Stage 2 feature and isn't wired up yet. Below is a
            preview of the domains already in the topic database.
          </p>
          <div className="chip-row">
            {domains?.domains?.map((d) => (
              <span className="chip" key={d.domain}>
                {d.domain} <span className="chip-count">{d.count}</span>
              </span>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>Your Profile</h2>
          <dl className="profile-grid">
            <dt>Name</dt>
            <dd>{me?.name}</dd>
            <dt>Email</dt>
            <dd>{me?.email}</dd>
            <dt>Role</dt>
            <dd>{me?.role}</dd>
          </dl>
        </div>
      </div>
    </div>
  )
}
