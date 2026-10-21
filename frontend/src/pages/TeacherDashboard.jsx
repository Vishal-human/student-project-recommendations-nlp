import { useEffect, useState, useCallback } from 'react'
import Navbar from '../components/Navbar.jsx'
import {
  getStudents, getTeacherDashboard,
  getPendingProposals, getAllProposals,
  approveProposal, rejectProposal,
  checkDuplicates
} from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

// ---------------------------------------------------------------------------
// Status styling
// ---------------------------------------------------------------------------
const STATUS_CONFIG = {
  pending:  { color: '#f59e0b', bg: '#f59e0b15', label: 'Pending' },
  approved: { color: '#22c55e', bg: '#22c55e15', label: 'Approved' },
  rejected: { color: '#ef4444', bg: '#ef444415', label: 'Rejected' },
}

const RISK_COLOR = { HIGH: '#ef4444', MEDIUM: '#f59e0b' }
const RISK_BG   = { HIGH: '#ef444415', MEDIUM: '#f59e0b15' }

// ---------------------------------------------------------------------------
// Proposal Card with approve/reject inline
// ---------------------------------------------------------------------------
function ProposalCard({ proposal, rank, onAction }) {
  const [rejectReason, setRejectReason] = useState('')
  const [showReject, setShowReject] = useState(false)
  const [acting, setActing] = useState(false)
  const cfg = STATUS_CONFIG[proposal.status]
  const isPending = proposal.status === 'pending'

  async function handleApprove() {
    setActing(true)
    try { await onAction('approve', proposal.id, '') }
    finally { setActing(false) }
  }

  async function handleReject() {
    setActing(true)
    try { await onAction('reject', proposal.id, rejectReason) }
    finally { setActing(false); setShowReject(false) }
  }

  return (
    <div style={{
      border: `1px solid ${cfg.color}44`, borderRadius: 10, padding: '14px 18px',
      marginBottom: 12, background: cfg.bg, position: 'relative'
    }}>
      {/* Priority badge for pending */}
      {isPending && (
        <span style={{
          position: 'absolute', top: 12, right: 14,
          background: '#6366f122', color: '#818cf8',
          fontSize: 11, fontWeight: 700, padding: '2px 8px',
          borderRadius: 999, border: '1px solid #6366f144'
        }}>
          #{rank} in queue
        </span>
      )}

      <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start', marginBottom: 8 }}>
        <span style={{
          fontSize: 12, fontWeight: 700, padding: '2px 10px', borderRadius: 999,
          color: cfg.color, background: cfg.color + '22', border: `1px solid ${cfg.color}44`
        }}>
          {cfg.label}
        </span>
      </div>

      <p style={{ margin: '0 0 4px', fontWeight: 700, fontSize: 15, color: '#e2e8f0' }}>
        {proposal.title}
      </p>
      <p style={{ margin: '0 0 8px', fontSize: 13, color: '#94a3b8' }}>
        <strong>{proposal.student_name}</strong> · {proposal.roll_no} · {proposal.student_email}
      </p>
      <p style={{ margin: '0 0 6px', fontSize: 12, color: '#64748b' }}>
        Submitted: {new Date(proposal.submitted_at).toLocaleString()}
        {proposal.reviewed_at && ` · Reviewed: ${new Date(proposal.reviewed_at).toLocaleString()}`}
      </p>
      {proposal.abstract && (
        <p style={{ margin: '0 0 8px', fontSize: 13, color: '#94a3b8', fontStyle: 'italic' }}>
          "{proposal.abstract.slice(0, 180)}{proposal.abstract.length > 180 ? '…' : ''}"
        </p>
      )}
      {proposal.reviewer_notes && (
        <p style={{ margin: '0 0 8px', fontSize: 13, color: '#64748b' }}>
          Note: <em>{proposal.reviewer_notes}</em>
        </p>
      )}

      {isPending && (
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 10 }}>
          <button
            onClick={handleApprove}
            disabled={acting}
            style={{
              background: '#22c55e', color: '#fff', border: 'none', borderRadius: 7,
              padding: '7px 20px', fontWeight: 600, fontSize: 13, cursor: acting ? 'not-allowed' : 'pointer'
            }}
          >
            ✓ Approve
          </button>
          <button
            onClick={() => setShowReject(v => !v)}
            disabled={acting}
            style={{
              background: '#ef4444', color: '#fff', border: 'none', borderRadius: 7,
              padding: '7px 20px', fontWeight: 600, fontSize: 13, cursor: 'pointer'
            }}
          >
            ✗ Reject
          </button>
          {showReject && (
            <div style={{ display: 'flex', gap: 6, width: '100%', marginTop: 6 }}>
              <input
                type="text"
                placeholder="Reason for rejection (optional)…"
                value={rejectReason}
                onChange={e => setRejectReason(e.target.value)}
                style={{
                  flex: 1, background: '#0d0d1a', border: '1px solid #3f3f5a', borderRadius: 7,
                  color: '#e2e8f0', padding: '6px 12px', fontSize: 13,
                }}
              />
              <button
                onClick={handleReject}
                disabled={acting}
                style={{
                  background: '#ef4444', color: '#fff', border: 'none', borderRadius: 7,
                  padding: '6px 14px', fontWeight: 600, fontSize: 13, cursor: 'pointer'
                }}
              >
                Confirm
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Duplicate pairs from auto-fetched proposals
// ---------------------------------------------------------------------------
function DuplicateCard({ pair }) {
  const color = RISK_COLOR[pair.risk_level]
  return (
    <div style={{
      border: `1px solid ${color}55`, borderRadius: 10, padding: '14px 18px',
      marginBottom: 10, background: RISK_BG[pair.risk_level]
    }}>
      <div style={{ marginBottom: 8 }}>
        <span style={{
          fontSize: 12, fontWeight: 700, color, background: color + '22',
          padding: '2px 10px', borderRadius: 999, border: `1px solid ${color}44`
        }}>
          {pair.risk_level} RISK — {pair.similarity_pct}% similar
        </span>
        <span style={{ color: '#64748b', fontSize: 12, marginLeft: 10 }}>
          ⚠️ Approve the EARLIER submission (shown left) — it has priority
        </span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        <div style={{ background: '#0d0d1a', borderRadius: 8, padding: '10px 14px' }}>
          <p style={{ margin: '0 0 2px', fontSize: 11, color: '#22c55e', fontWeight: 600 }}>PRIORITY (submitted first)</p>
          <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>
            {pair.student_a} · {pair.roll_a}
          </p>
          <p style={{ margin: 0, fontSize: 14, color: '#e2e8f0', fontWeight: 500 }}>{pair.title_a}</p>
        </div>
        <div style={{ background: '#0d0d1a', borderRadius: 8, padding: '10px 14px' }}>
          <p style={{ margin: '0 0 2px', fontSize: 11, color: '#f59e0b', fontWeight: 600 }}>LATER SUBMISSION</p>
          <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>
            {pair.student_b} · {pair.roll_b}
          </p>
          <p style={{ margin: 0, fontSize: 14, color: '#e2e8f0', fontWeight: 500 }}>{pair.title_b}</p>
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------
export default function TeacherDashboard() {
  const { auth } = useAuth()
  const [tab, setTab] = useState('proposals')
  const [students, setStudents] = useState([])
  const [data, setData] = useState(null)
  const [proposals, setProposals] = useState([])
  const [duplicates, setDuplicates] = useState(null)
  const [dupLoading, setDupLoading] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  const tabStyle = (active) => ({
    padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer',
    fontWeight: 600, fontSize: 14,
    background: active ? '#6366f1' : '#1e1e2d',
    color: active ? '#fff' : '#64748b',
    transition: 'all .15s',
  })

  const refresh = useCallback(() => {
    setRefreshKey(k => k + 1)
  }, [])

  useEffect(() => {
    getTeacherDashboard().then(setData).catch(() => {})
    getStudents().then(setStudents).catch(() => {})
    getAllProposals().then(setProposals).catch(() => {})
  }, [refreshKey])

  async function handleAction(action, id, notes) {
    try {
      if (action === 'approve') await approveProposal(id, notes)
      else await rejectProposal(id, notes)
      refresh()
    } catch (err) {
      alert(err.message || 'Action failed.')
    }
  }

  async function runDuplicateCheck() {
    const pending = proposals.filter(p => p.status === 'pending')
    if (pending.length < 2) {
      alert('Need at least 2 pending proposals to check for duplicates.')
      return
    }
    setDupLoading(true)
    try {
      // Auto-format — teacher doesn't type anything
      const topics = pending.map(p => ({
        student_name: p.student_name || 'Unknown',
        roll_no: p.roll_no || p.id.toString(),
        title: p.title,
        abstract: p.abstract || '',
      }))
      const result = await checkDuplicates(topics)
      setDuplicates(result)
    } catch (err) {
      alert(err.message || 'Duplicate check failed.')
    } finally {
      setDupLoading(false)
    }
  }

  const pending = proposals.filter(p => p.status === 'pending')
  const approved = proposals.filter(p => p.status === 'approved')
  const rejected = proposals.filter(p => p.status === 'rejected')

  return (
    <div>
      <Navbar />
      <div className="page">
        <h1>Supervisor Panel</h1>
        <p className="muted">Welcome, {auth?.name} — manage project proposals and detect duplicates.</p>

        {/* Stats */}
        <div className="stat-grid" style={{ marginBottom: 20 }}>
          {[
            { label: 'Total Proposals', value: proposals.length, color: '#6366f1' },
            { label: 'Pending Review', value: pending.length, color: '#f59e0b' },
            { label: 'Approved', value: approved.length, color: '#22c55e' },
            { label: 'Rejected', value: rejected.length, color: '#ef4444' },
          ].map(s => (
            <div className="stat-card" key={s.label}>
              <span className="stat-label">{s.label}</span>
              <span className="stat-value" style={{ color: s.color }}>{s.value}</span>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
          <button style={tabStyle(tab === 'proposals')} onClick={() => setTab('proposals')}>
            Proposals {pending.length > 0 && `(${pending.length} pending)`}
          </button>
          <button style={tabStyle(tab === 'duplicates')} onClick={() => setTab('duplicates')}>
            Duplicate Detector
          </button>
          <button style={tabStyle(tab === 'students')} onClick={() => setTab('students')}>
            Registered Students
          </button>
        </div>

        {/* ── Proposals Tab ── */}
        {tab === 'proposals' && (
          <div>
            {pending.length > 0 && (
              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <h2 style={{ margin: 0 }}>Pending Review ({pending.length})</h2>
                  <span style={{ fontSize: 12, color: '#64748b' }}>
                    Sorted by submission time — earlier = priority
                  </span>
                </div>
                {pending.map((p, i) => (
                  <ProposalCard key={p.id} proposal={p} rank={i + 1} onAction={handleAction} />
                ))}
              </div>
            )}
            {approved.length > 0 && (
              <div className="card">
                <h2>Approved ({approved.length})</h2>
                {approved.map(p => (
                  <ProposalCard key={p.id} proposal={p} rank={0} onAction={handleAction} />
                ))}
              </div>
            )}
            {rejected.length > 0 && (
              <div className="card">
                <h2>Rejected ({rejected.length})</h2>
                {rejected.map(p => (
                  <ProposalCard key={p.id} proposal={p} rank={0} onAction={handleAction} />
                ))}
              </div>
            )}
            {proposals.length === 0 && (
              <div className="card" style={{ textAlign: 'center', color: '#64748b', padding: '40px 20px' }}>
                <p style={{ fontSize: 18, marginBottom: 8 }}>No proposals yet</p>
                <p style={{ fontSize: 14 }}>Students' submitted proposals will appear here automatically.</p>
              </div>
            )}
          </div>
        )}

        {/* ── Duplicate Detector Tab ── */}
        {tab === 'duplicates' && (
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
              <div>
                <h2 style={{ margin: '0 0 6px' }}>Duplicate Detector</h2>
                <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>
                  Automatically loads all {pending.length} pending submissions — no manual input needed.
                </p>
              </div>
              <button
                onClick={runDuplicateCheck}
                disabled={dupLoading || pending.length < 2}
                style={{
                  background: pending.length < 2 ? '#1e1e2d' : '#6366f1',
                  color: pending.length < 2 ? '#3f3f5a' : '#fff',
                  border: 'none', borderRadius: 8, padding: '10px 20px',
                  fontWeight: 600, fontSize: 14, cursor: pending.length < 2 ? 'not-allowed' : 'pointer',
                }}
              >
                {dupLoading ? 'Analysing…' : `Check ${pending.length} Submissions`}
              </button>
            </div>

            {/* Preview of loaded submissions */}
            <div style={{ background: '#0d0d1a', borderRadius: 8, padding: 14, marginBottom: 16 }}>
              <p style={{ margin: '0 0 8px', fontSize: 13, color: '#64748b', fontWeight: 600 }}>
                Submissions loaded automatically ({pending.length}):
              </p>
              {pending.length === 0 ? (
                <p style={{ margin: 0, color: '#3f3f5a', fontSize: 13 }}>No pending proposals to check.</p>
              ) : (
                <ul style={{ margin: 0, padding: '0 0 0 18px', color: '#94a3b8', fontSize: 13 }}>
                  {pending.map((p, i) => (
                    <li key={p.id} style={{ marginBottom: 4 }}>
                      <strong style={{ color: '#e2e8f0' }}>{p.student_name}</strong>
                      {' '}({p.roll_no}) — {p.title}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {duplicates && (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 20 }}>
                  {[
                    { label: 'Checked', value: duplicates.total_submissions, color: '#6366f1' },
                    { label: 'Flagged Pairs', value: duplicates.flagged_pairs.length, color: duplicates.flagged_pairs.length > 0 ? '#ef4444' : '#22c55e' },
                    { label: 'Unique Topics', value: duplicates.clean_topics, color: '#22c55e' },
                  ].map(s => (
                    <div key={s.label} style={{ background: '#13131f', borderRadius: 8, padding: '12px 16px', border: '1px solid #2e2e3a' }}>
                      <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>{s.label}</p>
                      <p style={{ margin: 0, fontSize: 26, fontWeight: 700, color: s.color }}>{s.value}</p>
                    </div>
                  ))}
                </div>
                {duplicates.flagged_pairs.length === 0 ? (
                  <p style={{ color: '#22c55e', fontWeight: 600, textAlign: 'center', padding: '20px 0' }}>
                    ✓ No near-duplicates found. All topics appear unique.
                  </p>
                ) : (
                  <>
                    <p style={{ color: '#f87171', fontSize: 14, marginBottom: 12 }}>
                      {duplicates.flagged_pairs.length} duplicate pair(s) detected — approve the student listed on the LEFT (submitted earlier).
                    </p>
                    {duplicates.flagged_pairs.map((pair, i) => (
                      <DuplicateCard key={i} pair={pair} />
                    ))}
                  </>
                )}
              </>
            )}
          </div>
        )}

        {/* ── Students Tab ── */}
        {tab === 'students' && (
          <div className="card">
            <h2>Registered Students ({students.length})</h2>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Joined</th>
                </tr>
              </thead>
              <tbody>
                {students.map(s => (
                  <tr key={s.id}>
                    <td>{s.name}</td>
                    <td>{s.email}</td>
                    <td>{new Date(s.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
                {students.length === 0 && (
                  <tr><td colSpan={3} className="muted">No students registered yet.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
