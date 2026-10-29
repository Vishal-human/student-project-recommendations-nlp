import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login as loginApi } from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

const ROLE_LABEL = { student: 'Student', teacher: 'Teacher', supervisor: 'Supervisor' }

export default function Login() {
  const [role, setRole] = useState('student')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const data = await loginApi({ email, password })
      if (data.role !== role) {
        setError(
          `This account is registered as a ${data.role}. Switch to "${
            ROLE_LABEL[data.role] || 'Student'
          }" above and log in again.`,
        )
        return
      }
      login(data)
      navigate(`/${data.role}`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-card">
      <div className="brand">Topic Recommender</div>
      <h1>Log In</h1>

      <div className="role-toggle" role="tablist" aria-label="Login as">
        <button
          type="button"
          role="tab"
          aria-selected={role === 'student'}
          className={role === 'student' ? 'active' : ''}
          onClick={() => setRole('student')}
        >
          Student
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={role === 'teacher'}
          className={role === 'teacher' ? 'active' : ''}
          onClick={() => setRole('teacher')}
        >
          Teacher
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={role === 'supervisor'}
          className={role === 'supervisor' ? 'active' : ''}
          onClick={() => setRole('supervisor')}
        >
          Supervisor
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error && <p className="error">{error}</p>}
        <div className="row-between">
          <Link className="link-muted" to="/forgot-password">
            Forgot password?
          </Link>
        </div>
        <button type="submit">Log In as {ROLE_LABEL[role]}</button>
      </form>

      {role === 'student' && (
        <p>
          New student? <Link to="/signup">Create an account</Link>
        </p>
      )}
      {role !== 'student' && (
        <p className="muted">{ROLE_LABEL[role]} accounts are set up by the project team, not self-registered.</p>
      )}
    </div>
  )
}
