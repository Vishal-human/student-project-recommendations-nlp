import { useEffect, useState, useCallback } from 'react'
import Navbar from '../components/Navbar.jsx'
import {
  getDomains, getMe, getStudentDashboard,
  getRecommendations, generateTopics, submitProposal, getMyProposals
} from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

const TAG_LIST = [
  'javascript', 'typescript', 'python', 'html', 'css',
  'react', 'nodejs', 'fastapi', 'flask', 'django',
  'docker', 'sql', 'mongodb', 'firebase',
  'nlp', 'computer-vision', 'machine-learning', 'deep-learning',
  'data-analysis', 'api-integration',
]

const STATUS_CONFIG = {
  pending:  { color: '#f59e0b', bg: '#f59e0b15', label: '⏳ Pending Review' },
  approved: { color: '#22c55e', bg: '#22c55e15', label: '✅ Approved' },
  rejected: { color: '#ef4444', bg: '#ef444415', label: '❌ Rejected — Please resubmit' },
}

// ---------------------------------------------------------------------------
// Components
// ---------------------------------------------------------------------------

function InstructionsModal({ onClose }) {
  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center',
      justifyContent: 'center', zIndex: 9999, padding: 20
    }}>
      <div style={{
        background: '#1e1e2d', border: '1px solid #3f3f5a', borderRadius: 12,
        padding: 28, maxWidth: 580, width: '100%', color: '#e2e8f0',
        boxShadow: '0 10px 25px rgba(0,0,0,0.5)'
      }}>
        <h2 style={{ marginTop: 0, marginBottom: 4 }}>How TopicMatch Works</h2>
        <p style={{ color: '#64748b', fontSize: 13, marginBottom: 18 }}>
          Your AI-powered project guide for university submissions
        </p>
        <ol style={{ lineHeight: 2, color: '#e2e8f0', paddingLeft: 20, marginBottom: 20 }}>
          <li>Describe your <strong>interests</strong> and pick your <strong>tech stack</strong></li>
          <li>Get personalised project recommendations ranked by:
            <ul style={{ color: '#94a3b8', lineHeight: 1.9, marginTop: 4 }}>
              <li><strong style={{color:'#6366f1'}}>Relevance</strong> — how well it matches what you asked for</li>
              <li><strong style={{color:'#22c55e'}}>Novelty (0-100)</strong> — how unique it is vs past submissions</li>
              <li><strong style={{color:'#f59e0b'}}>Feasibility (0-100)</strong> — realistic for your team size & timeline</li>
            </ul>
          </li>
          <li><strong>Select and submit</strong> a proposal — your supervisor reviews it</li>
          <li>Once approved, that topic is <strong>reserved for you</strong> and hidden from other students</li>
        </ol>
        <button onClick={onClose} style={{
          background: '#6366f1', color: '#fff', border: 'none', padding: '10px 20px',
          borderRadius: 8, cursor: 'pointer', fontWeight: 600, width: '100%'
        }}>
          Got it, let's start!
        </button>
      </div>
    </div>
  )
}

function ScoreBadge({ score, label }) {
  const color = score >= 70 ? '#22c55e' : score >= 40 ? '#f59e0b' : '#ef4444'
  return (
    <span style={{
      display: 'inline-block', padding: '2px 10px', borderRadius: 999,
      background: color + '22', color, fontWeight: 700, fontSize: 13,
      border: `1px solid ${color}55`,
    }}>
      {label}: {score}/100
    </span>
  )
}

function ResultCard({ item, onSubmit, submitting, hasActiveProposal }) {
  const [expanded, setExpanded] = useState(false)
  return (
    <div style={{
      border: '1px solid #2e2e3a', borderRadius: 12, padding: '16px 20px',
      marginBottom: 14, background: '#13131f',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8 }}>
        <h3 style={{ margin: 0, fontSize: 16, color: '#e2e8f0' }}>{item.title}</h3>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <ScoreBadge score={item.novelty_score} label="Novelty" />
          <ScoreBadge score={item.feasibility_score} label="Feasibility" />
        </div>
      </div>
      <p style={{ margin: '10px 0 8px', color: '#94a3b8', fontSize: 14, lineHeight: 1.5 }}>
        {item.explanation}
      </p>
      {item.missing_skills.length > 0 && (
        <p style={{ margin: '4px 0', fontSize: 13, color: '#f87171' }}>
          ⚠️ Missing skills: {item.missing_skills.join(', ')}
        </p>
      )}
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 8 }}>
        {item.suggested_stack.map(t => (
          <span key={t} className="chip" style={{ fontSize: 12 }}>{t}</span>
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
        <button
          onClick={() => setExpanded(e => !e)}
          style={{ background: 'none', border: 'none', color: '#6366f1', cursor: 'pointer', fontSize: 13, padding: 0 }}
        >
          {expanded ? '▲ Hide' : '▼ Show'} nearest historical matches
        </button>
        <button
          onClick={() => onSubmit(item)}
          disabled={submitting || hasActiveProposal}
          title={hasActiveProposal ? 'You already have an active proposal' : 'Submit this as your project proposal'}
          style={{
            background: hasActiveProposal ? '#1e1e2d' : '#6366f1',
            color: hasActiveProposal ? '#3f3f5a' : '#fff',
            border: hasActiveProposal ? '1px solid #3f3f5a' : 'none',
            borderRadius: 8, padding: '6px 18px', fontSize: 13, fontWeight: 600,
            cursor: hasActiveProposal ? 'not-allowed' : 'pointer',
            transition: 'all .15s',
          }}
        >
          {submitting ? 'Submitting…' : hasActiveProposal ? 'Already submitted' : '📋 Submit Proposal'}
        </button>
      </div>
      {expanded && (
        <ul style={{ margin: '8px 0 0 0', padding: '0 0 0 20px', color: '#94a3b8', fontSize: 13 }}>
          {item.nearest_matches.map((m, i) => (
            <li key={i}>{m.title} ({m.year}) — {m.similarity_pct}% similar</li>
          ))}
        </ul>
      )}
    </div>
  )
}

function ProposalStatusBanner({ proposals, onRefresh }) {
  if (!proposals || proposals.length === 0) return null
  const latest = proposals[0]
  const cfg = STATUS_CONFIG[latest.status]
  return (
    <div style={{
      border: `1px solid ${cfg.color}44`, borderRadius: 10,
      padding: '14px 18px', background: cfg.bg, marginBottom: 20,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontWeight: 700, color: cfg.color, fontSize: 14 }}>{cfg.label}</span>
          <p style={{ margin: '4px 0 0', color: '#e2e8f0', fontSize: 15, fontWeight: 600 }}>
            "{latest.title}"
          </p>
          <p style={{ margin: '4px 0 0', color: '#64748b', fontSize: 12 }}>
            Submitted: {new Date(latest.submitted_at).toLocaleString()}
          </p>
          {latest.reviewer_notes && (
            <p style={{ margin: '6px 0 0', color: '#94a3b8', fontSize: 13 }}>
              Supervisor note: <em>{latest.reviewer_notes}</em>
            </p>
          )}
        </div>
        <button onClick={onRefresh} style={{
          background: 'none', border: '1px solid #3f3f5a', color: '#94a3b8',
          borderRadius: 6, padding: '4px 12px', cursor: 'pointer', fontSize: 12
        }}>↻ Refresh</button>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function StudentDashboard() {
  const { auth } = useAuth()
  const [dashboard, setDashboard] = useState(null)
  const [me, setMe] = useState(null)
  const [domains, setDomains] = useState(null)
  const [myProposals, setMyProposals] = useState([])

  const [interests, setInterests] = useState('')
  const [ownIdea, setOwnIdea] = useState('')
  const [stack, setStack] = useState([])
  const [timeBudget, setTimeBudget] = useState(4)
  const [teamSize, setTeamSize] = useState(2)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [generated, setGenerated] = useState(null)
  const [genNotice, setGenNotice] = useState('')
  const [genLoading, setGenLoading] = useState(false)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitMsg, setSubmitMsg] = useState('')

  const [showInstructions, setShowInstructions] = useState(() =>
    localStorage.getItem('hideInstructions') !== 'true'
  )

  const hasActiveProposal = myProposals.some(
    p => p.status === 'pending' || p.status === 'approved'
  )

  const refreshProposals = useCallback(() => {
    getMyProposals().then(setMyProposals).catch(() => {})
  }, [])

  useEffect(() => {
    getStudentDashboard().then(setDashboard).catch(() => {})
    getMe().then(setMe).catch(() => {})
    getDomains().then(setDomains).catch(() => {})
    refreshProposals()
  }, [refreshProposals])

  function closeInstructions() {
    localStorage.setItem('hideInstructions', 'true')
    setShowInstructions(false)
  }

  function toggleTag(tag) {
    setStack(s => s.includes(tag) ? s.filter(t => t !== tag) : [...s, tag])
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!interests.trim() && !ownIdea.trim()) {
      setError('Please describe your interests or paste your own idea.')
      return
    }
    setError('')
    setLoading(true)
    setResults(null)
    try {
      const res = await getRecommendations({
        interests: interests.trim(),
        own_idea: ownIdea.trim() || null,
        stack,
        time_budget_weeks: Number(timeBudget),
        team_size: Number(teamSize),
      })
      setResults(res.recommendations)
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  async function handleGenerate() {
    if (!interests.trim()) {
      setError('Describe your interests first so new ideas can be generated.')
      return
    }
    setError('')
    setGenLoading(true)
    setGenerated(null)
    try {
      const res = await generateTopics({
        interests: interests.trim(),
        stack,
        time_budget_weeks: Number(timeBudget),
        team_size: Number(teamSize),
      })
      setGenerated(res.recommendations)
      setGenNotice(res.notice)
    } catch (err) {
      setError(err.message || 'Could not generate ideas. Please try again.')
    } finally {
      setGenLoading(false)
    }
  }

  async function handleProposalSubmit(item) {
    if (hasActiveProposal) return
    setSubmitting(true)
    setSubmitMsg('')
    try {
      await submitProposal({
        title: item.title,
        abstract: item.explanation,
        interest_desc: interests,
        stack_tags: stack,
      })
      setSubmitMsg(`✅ "${item.title}" submitted for review! Your supervisor will approve or reject it.`)
      refreshProposals()
    } catch (err) {
      setSubmitMsg('❌ ' + (err.message || 'Failed to submit. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  async function handleOwnIdeaSubmit() {
    if (!ownIdea.trim()) {
      setError('Enter your project idea first.')
      return
    }
    if (hasActiveProposal) return
    setSubmitting(true)
    setSubmitMsg('')
    try {
      await submitProposal({
        title: ownIdea.trim(),
        abstract: '',
        interest_desc: interests,
        stack_tags: stack,
      })
      setSubmitMsg(`✅ Your idea "${ownIdea.trim()}" has been submitted for review!`)
      refreshProposals()
    } catch (err) {
      setSubmitMsg('❌ ' + (err.message || 'Failed to submit.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      {showInstructions && <InstructionsModal onClose={closeInstructions} />}
      <Navbar />
      <div className="page">
        <h1>Welcome, {auth?.name}</h1>
        <p className="muted">{dashboard?.next_step}</p>

        {/* My Proposal Status Banner */}
        {myProposals.length > 0 && (
          <ProposalStatusBanner proposals={myProposals} onRefresh={refreshProposals} />
        )}

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

        {/* NLP Recommender */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
            <h2 style={{ margin: 0 }}>Find Your Project Topic</h2>
            <button
              onClick={() => setShowInstructions(true)}
              style={{
                background: '#2e2e3a', color: '#94a3b8', border: 'none',
                borderRadius: '50%', width: 24, height: 24, display: 'flex',
                alignItems: 'center', justifyContent: 'center', cursor: 'pointer',
                fontWeight: 'bold', fontSize: 14
              }}
              title="How scoring works"
            >?</button>
          </div>

          {hasActiveProposal && (
            <div style={{
              background: '#6366f110', border: '1px solid #6366f133', borderRadius: 8,
              padding: '10px 14px', marginBottom: 16, fontSize: 13, color: '#818cf8'
            }}>
              ℹ️ You already have an active proposal. You can still browse for reference, but you cannot submit another until your supervisor reviews the current one.
            </div>
          )}

          <p className="muted" style={{ marginBottom: 20 }}>
            Describe your interests — we'll rank project ideas by novelty and feasibility.
            Topics already claimed by other students are automatically excluded.
          </p>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <span style={{ color: '#94a3b8', fontSize: 14 }}>Your interests / project description *</span>
              <textarea
                value={interests}
                onChange={e => setInterests(e.target.value)}
                rows={3}
                placeholder="e.g. I'm interested in NLP and want to build something useful for HR departments..."
                style={{
                  background: '#0d0d1a', border: '1px solid #2e2e3a', borderRadius: 8,
                  color: '#e2e8f0', padding: '10px 14px', resize: 'vertical', fontSize: 14,
                }}
              />
            </label>

            <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <span style={{ color: '#94a3b8', fontSize: 14 }}>Already have your own idea? (optional)</span>
              <div style={{ display: 'flex', gap: 8 }}>
                <input
                  type="text"
                  value={ownIdea}
                  onChange={e => setOwnIdea(e.target.value)}
                  placeholder="e.g. AI-based resume screener using BERT"
                  style={{
                    flex: 1, background: '#0d0d1a', border: '1px solid #2e2e3a', borderRadius: 8,
                    color: '#e2e8f0', padding: '10px 14px', fontSize: 14,
                  }}
                />
                <button
                  type="button"
                  onClick={handleOwnIdeaSubmit}
                  disabled={submitting || hasActiveProposal || !ownIdea.trim()}
                  style={{
                    background: hasActiveProposal ? '#1e1e2d' : '#4f46e5',
                    color: hasActiveProposal ? '#3f3f5a' : '#fff',
                    border: 'none', borderRadius: 8, padding: '10px 16px',
                    fontSize: 13, fontWeight: 600, cursor: hasActiveProposal || !ownIdea.trim() ? 'not-allowed' : 'pointer',
                    whiteSpace: 'nowrap',
                  }}
                >
                  Submit This Idea
                </button>
              </div>
            </label>

            <div>
              <span style={{ color: '#94a3b8', fontSize: 14, display: 'block', marginBottom: 8 }}>Your tech stack</span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {TAG_LIST.map(tag => (
                  <button
                    key={tag} type="button" onClick={() => toggleTag(tag)}
                    style={{
                      padding: '4px 14px', borderRadius: 999, fontSize: 13, cursor: 'pointer',
                      border: stack.includes(tag) ? '1.5px solid #6366f1' : '1px solid #2e2e3a',
                      background: stack.includes(tag) ? '#6366f120' : '#13131f',
                      color: stack.includes(tag) ? '#818cf8' : '#64748b',
                      transition: 'all .15s',
                    }}
                  >{tag}</button>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
              <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <span style={{ color: '#94a3b8', fontSize: 14 }}>Time budget (weeks)</span>
                <input
                  type="number" min={1} max={52} value={timeBudget}
                  onChange={e => setTimeBudget(e.target.value)}
                  style={{
                    width: 90, background: '#0d0d1a', border: '1px solid #2e2e3a',
                    borderRadius: 8, color: '#e2e8f0', padding: '8px 12px', fontSize: 14,
                  }}
                />
              </label>
              <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <span style={{ color: '#94a3b8', fontSize: 14 }}>Team size</span>
                <input
                  type="number" min={1} max={10} value={teamSize}
                  onChange={e => setTeamSize(e.target.value)}
                  style={{
                    width: 90, background: '#0d0d1a', border: '1px solid #2e2e3a',
                    borderRadius: 8, color: '#e2e8f0', padding: '8px 12px', fontSize: 14,
                  }}
                />
              </label>
            </div>

            {error && <p style={{ color: '#f87171', margin: 0, fontSize: 14 }}>{error}</p>}
            {submitMsg && (
              <p style={{ color: submitMsg.startsWith('✅') ? '#22c55e' : '#f87171', margin: 0, fontSize: 14 }}>
                {submitMsg}
              </p>
            )}

            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <button
                type="submit" disabled={loading}
                style={{
                  background: loading ? '#3730a3' : '#6366f1',
                  color: '#fff', border: 'none', borderRadius: 8, padding: '10px 28px',
                  fontSize: 15, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer',
                }}
              >
                {loading ? 'Finding topics…' : 'Get Recommendations'}
              </button>
              <button
                type="button" onClick={handleGenerate} disabled={genLoading}
                title="Create brand-new topics in your interest area that don't exist in the database"
                style={{
                  background: 'transparent', color: '#818cf8', border: '1.5px solid #6366f1',
                  borderRadius: 8, padding: '10px 28px', fontSize: 15, fontWeight: 600,
                  cursor: genLoading ? 'not-allowed' : 'pointer',
                }}
              >
                {genLoading ? 'Generating ideas…' : '✨ Generate New Ideas'}
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        {results && (
          <div className="card">
            <h2>Recommendations ({results.length})</h2>
            {results.length === 0 ? (
              <p style={{ color: '#64748b' }}>No available topics match your search — some may have been claimed by other students. Try different keywords.</p>
            ) : (
              results.map((item, i) => (
                <ResultCard
                  key={i}
                  item={item}
                  onSubmit={handleProposalSubmit}
                  submitting={submitting}
                  hasActiveProposal={hasActiveProposal}
                />
              ))
            )}
          </div>
        )}

        {generated && (
          <div className="card">
            <h2>✨ New Ideas ({generated.length})</h2>
            {genNotice && <p style={{ color: '#94a3b8', fontSize: 13, marginTop: 0 }}>{genNotice}</p>}
            {generated.length === 0 ? (
              <p style={{ color: '#64748b' }}>No sufficiently new ideas this time — try rewording your interests and generate again.</p>
            ) : (
              generated.map((item, i) => (
                <ResultCard
                  key={i}
                  item={item}
                  onSubmit={handleProposalSubmit}
                  submitting={submitting}
                  hasActiveProposal={hasActiveProposal}
                />
              ))
            )}
          </div>
        )}

        {/* Domain preview */}
        <div className="card">
          <h2>Topic Domains in Database</h2>
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
            <dt>Name</dt><dd>{me?.name}</dd>
            <dt>Email</dt><dd>{me?.email}</dd>
            <dt>Role</dt><dd>{me?.role}</dd>
          </dl>
        </div>
      </div>
    </div>
  )
}
