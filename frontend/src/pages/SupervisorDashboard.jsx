import { useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import { checkDuplicates } from '../api.js'

const RISK_COLOR = { HIGH: '#ef4444', MEDIUM: '#f59e0b' }
const RISK_BG   = { HIGH: '#ef444415', MEDIUM: '#f59e0b15' }

function DuplicateCard({ pair }) {
  const color = RISK_COLOR[pair.risk_level]
  const bg    = RISK_BG[pair.risk_level]
  return (
    <div style={{
      border: `1px solid ${color}55`, borderRadius: 10, padding: '14px 18px',
      marginBottom: 12, background: bg,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <span style={{
          fontSize: 12, fontWeight: 700, letterSpacing: 1,
          color, background: color + '22', padding: '2px 10px', borderRadius: 999,
          border: `1px solid ${color}44`
        }}>
          {pair.risk_level} RISK — {pair.similarity_pct}% similar
        </span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <div style={{ background: '#0d0d1a', borderRadius: 8, padding: '10px 14px' }}>
          <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>
            {pair.student_a} · {pair.roll_a}
          </p>
          <p style={{ margin: 0, fontSize: 14, color: '#e2e8f0', fontWeight: 500 }}>{pair.title_a}</p>
        </div>
        <div style={{ background: '#0d0d1a', borderRadius: 8, padding: '10px 14px' }}>
          <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>
            {pair.student_b} · {pair.roll_b}
          </p>
          <p style={{ margin: 0, fontSize: 14, color: '#e2e8f0', fontWeight: 500 }}>{pair.title_b}</p>
        </div>
      </div>
    </div>
  )
}

// Parse CSV-style input: Name, RollNo, Title, Abstract(optional)
function parseTopics(raw) {
  return raw.trim().split('\n')
    .filter(l => l.trim())
    .map((line, i) => {
      const parts = line.split(',').map(p => p.trim())
      return {
        student_name: parts[0] || `Student ${i + 1}`,
        roll_no: parts[1] || `R${i + 1}`,
        title: parts[2] || parts[0],
        abstract: parts[3] || '',
      }
    })
}

const DEMO_INPUT = `Priya Sharma, 22IMCA01, AI-Based Resume Screening Tool
Ravi Patel, 22IMCA02, Automated Resume Screening using Machine Learning
Anjali Mehta, 22IMCA03, Face Recognition Attendance System
Karan Joshi, 22IMCA04, Attendance Marking using Facial Recognition
Deepak Shah, 22IMCA05, Stock Price Prediction using LSTM
Neha Trivedi, 22IMCA06, Sentiment Analysis of Product Reviews
Arjun Verma, 22IMCA07, Twitter Sentiment Analysis
Pooja Gupta, 22IMCA08, Smart Traffic Signal with Computer Vision
Rohit Desai, 22IMCA09, Fake News Detection using NLP
Sonal Modi, 22IMCA10, Real-time Object Detection for Blind Assistance`

export default function SupervisorDashboard({ embedded = false }) {
  const [input, setInput] = useState(DEMO_INPUT)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function handleCheck() {
    const topics = parseTopics(input)
    if (topics.length < 2) {
      setError('Enter at least 2 topics, one per line.')
      return
    }
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const data = await checkDuplicates(topics)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const content = (
    <>
      {!embedded && (
        <div style={{ marginBottom: 8 }}>
          <h1 style={{ margin: '0 0 4px' }}>Supervisor Dashboard</h1>
          <p className="muted">
            Paste submitted project topics and detect near-duplicates using AI semantic matching —
            catches paraphrased duplicates that manual spreadsheet review misses.
          </p>
        </div>
      )}

        {/* How it works callout */}
        <div style={{
          background: '#6366f110', border: '1px solid #6366f133', borderRadius: 10,
          padding: '12px 18px', marginBottom: 20, fontSize: 14, color: '#94a3b8', lineHeight: 1.6,
        }}>
          <strong style={{ color: '#818cf8' }}>How it works:</strong> Enter one student per line in
          the format: <code style={{ color: '#e2e8f0' }}>Name, Roll No, Project Title</code>.
          The system embeds each title using the same AI model as the student recommender and
          flags pairs with semantic similarity above 75% as potential duplicates.
        </div>

        <div className="card">
          <h2 style={{ marginTop: 0 }}>Submit Batch for Review</h2>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            rows={12}
            placeholder="Priya Sharma, 22IMCA01, AI-Based Resume Screening Tool"
            style={{
              width: '100%', background: '#0d0d1a', border: '1px solid #2e2e3a', borderRadius: 8,
              color: '#e2e8f0', padding: '10px 14px', fontSize: 13, fontFamily: 'monospace',
              resize: 'vertical', boxSizing: 'border-box', marginBottom: 12,
            }}
          />
          {error && <p style={{ color: '#f87171', fontSize: 14, margin: '0 0 12px' }}>{error}</p>}
          <button
            onClick={handleCheck}
            disabled={loading}
            style={{
              background: loading ? '#3730a3' : '#6366f1', color: '#fff', border: 'none',
              borderRadius: 8, padding: '10px 28px', fontSize: 15, fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Analysing…' : 'Check for Duplicates'}
          </button>
        </div>

        {result && (
          <div className="card">
            {/* Summary stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, marginBottom: 24 }}>
              {[
                { label: 'Total Submissions', value: result.total_submissions, color: '#6366f1' },
                { label: 'Flagged Pairs', value: result.flagged_pairs.length, color: result.flagged_pairs.length > 0 ? '#ef4444' : '#22c55e' },
                { label: 'Clean Topics', value: result.clean_topics, color: '#22c55e' },
              ].map(s => (
                <div key={s.label} style={{ background: '#13131f', borderRadius: 10, padding: '14px 18px', border: '1px solid #2e2e3a' }}>
                  <p style={{ margin: '0 0 4px', fontSize: 12, color: '#64748b' }}>{s.label}</p>
                  <p style={{ margin: 0, fontSize: 28, fontWeight: 700, color: s.color }}>{s.value}</p>
                </div>
              ))}
            </div>

            {result.flagged_pairs.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '24px 0', color: '#22c55e' }}>
                <p style={{ fontSize: 20, fontWeight: 700, margin: '0 0 8px' }}>✓ No duplicates detected</p>
                <p style={{ color: '#64748b', margin: 0 }}>All {result.total_submissions} submissions appear sufficiently unique.</p>
              </div>
            ) : (
              <>
                <h3 style={{ marginTop: 0, color: '#f87171' }}>
                  {result.flagged_pairs.length} flagged pair{result.flagged_pairs.length > 1 ? 's' : ''}
                </h3>
                {result.flagged_pairs.map((pair, i) => (
                  <DuplicateCard key={i} pair={pair} />
                ))}
              </>
            )}
          </div>
        )}
      </>
  )

  if (embedded) return content
  return (
    <div>
      <Navbar />
      <div className="page">{content}</div>
    </div>
  )
}
