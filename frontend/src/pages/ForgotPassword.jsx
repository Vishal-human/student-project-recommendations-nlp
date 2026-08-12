import { useState } from 'react'
import { Link } from 'react-router-dom'
import { forgotPassword } from '../api.js'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await forgotPassword({ email })
      setSent(true)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-card">
      <div className="brand">Topic Recommender</div>
      <h1>Forgot Password</h1>

      {sent ? (
        <>
          <p>If that email is registered, a reset link has been generated.</p>
          <p className="muted">
            Dev note: no email service is set up yet, so the reset link is printed to the
            backend's console log instead of being emailed. Check the terminal running the
            backend for a line starting with <code>[password reset]</code>.
          </p>
        </>
      ) : (
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          {error && <p className="error">{error}</p>}
          <button type="submit">Send Reset Link</button>
        </form>
      )}

      <p>
        <Link to="/login">Back to Log In</Link>
      </p>
    </div>
  )
}
