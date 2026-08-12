import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { resetPassword } from '../api.js'

export default function ResetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') || ''
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [done, setDone] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (password !== confirm) {
      setError('Passwords do not match.')
      return
    }
    try {
      await resetPassword({ token, new_password: password })
      setDone(true)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-card">
      <div className="brand">Topic Recommender</div>
      <h1>Reset Password</h1>

      {!token && <p className="error">No reset token found in the link. Request a new one.</p>}

      {done ? (
        <p>Your password has been reset. You can now log in.</p>
      ) : (
        token && (
          <form onSubmit={handleSubmit}>
            <label>New Password</label>
            <input
              type="password"
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <label>Confirm New Password</label>
            <input
              type="password"
              minLength={6}
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              required
            />
            {error && <p className="error">{error}</p>}
            <button type="submit">Reset Password</button>
          </form>
        )
      )}

      <p>
        <Link to="/login">Back to Log In</Link>
      </p>
    </div>
  )
}
