import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import SupervisorDashboard from './SupervisorDashboard.jsx'
import DatasetUploader from '../components/DatasetUploader.jsx'
import { getSupervisorDashboard, getAllProposals } from '../api.js'

const STATUS_COLOR = { pending: '#f59e0b', approved: '#22c55e', rejected: '#ef4444' }

function Stat({ label, value, color = '#818cf8' }) {
  return (
    <div style={{ background: '#13131f', borderRadius: 10, padding: '14px 18px', border: '1px solid #2e2e3a' }}>
      <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>{label}</p>
      <p style={{ margin: 0, fontSize: 28, fontWeight: 700, color }}>{value}</p>
    </div>
  )
}

export default function SupervisorHome() {
  const [overview, setOverview] = useState(null)
  const [proposals, setProposals] = useState([])
  const [tab, setTab] = useState('overview')
  const [error, setError] = useState('')

  useEffect(() => {
    getSupervisorDashboard().then(setOverview).catch(e => setError(e.message))
    getAllProposals().then(setProposals).catch(() => {})
  }, [])

  const tabStyle = (active) => ({
    background: active ? '#6366f1' : 'transparent', color: active ? '#fff' : '#94a3b8',
    border: '1px solid #2e2e3a', borderRadius: 8, padding: '8px 18px', cursor: 'pointer', fontWeight: 600,
  })

  return (
    <div>
      <Navbar />
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, flexWrap: 'wrap', gap: 12 }}>
          <div>
            <h1 style={{ margin: '0 0 4px' }}>Supervisor Dashboard</h1>
            <p className="muted" style={{ margin: 0 }}>
              Institution-level oversight: see all proposals, upload corpus dataset files, and run the AI duplicate detector.
            </p>
          </div>
          <button
            onClick={() => setTab('dataset')}
            style={{
              background: tab === 'dataset' ? '#22c55e' : '#6366f1',
              color: '#fff',
              border: 'none',
              borderRadius: 8,
              padding: '10px 18px',
              fontWeight: 600,
              fontSize: 14,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              boxShadow: '0 4px 12px rgba(99, 102, 241, 0.25)'
            }}
          >
            📁 + Add Data File
          </button>
        </div>
        {error && <p style={{ color: '#f87171' }}>{error}</p>}

        <div style={{ display: 'flex', gap: 10, margin: '16px 0', flexWrap: 'wrap' }}>
          <button style={tabStyle(tab === 'overview')} onClick={() => setTab('overview')}>Overview</button>
          <button style={tabStyle(tab === 'dataset')} onClick={() => setTab('dataset')}>📁 Add Data File (Corpus)</button>
          <button style={tabStyle(tab === 'proposals')} onClick={() => setTab('proposals')}>All Proposals</button>
          <button style={tabStyle(tab === 'duplicates')} onClick={() => setTab('duplicates')}>Duplicate Detector</button>
        </div>

        {tab === 'overview' && overview && (
          <div className="card">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 14 }}>
              <Stat label="Students" value={overview.students} />
              <Stat label="Teachers" value={overview.teachers} />
              <Stat label="Total proposals" value={overview.proposals.total} />
              <Stat label="Pending" value={overview.proposals.pending} color={STATUS_COLOR.pending} />
              <Stat label="Approved" value={overview.proposals.approved} color={STATUS_COLOR.approved} />
              <Stat label="Rejected" value={overview.proposals.rejected} color={STATUS_COLOR.rejected} />
            </div>
          </div>
        )}

        {tab === 'dataset' && <DatasetUploader />}

        {tab === 'proposals' && (
          <div className="card">
            <h2 style={{ marginTop: 0 }}>All Proposals ({proposals.length})</h2>
            {proposals.length === 0 ? (
              <p style={{ color: '#64748b' }}>No proposals submitted yet.</p>
            ) : proposals.map(p => (
              <div key={p.id} style={{ borderBottom: '1px solid #2e2e3a', padding: '10px 0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
                  <strong style={{ color: '#e2e8f0' }}>{p.title}</strong>
                  <span style={{ color: STATUS_COLOR[p.status], fontWeight: 600, textTransform: 'capitalize' }}>{p.status}</span>
                </div>
                <p style={{ margin: '4px 0 0', fontSize: 13, color: '#64748b' }}>
                  {p.student_name} · {p.roll_no} · submitted {new Date(p.submitted_at).toLocaleString()}
                  {p.reviewer_notes ? ` · note: ${p.reviewer_notes}` : ''}
                </p>
              </div>
            ))}
          </div>
        )}

        {tab === 'duplicates' && <SupervisorDashboard embedded />}
      </div>
    </div>
  )
}
