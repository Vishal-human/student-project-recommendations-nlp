import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup as signupApi } from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function Signup() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const data = await signupApi({ name, email, password })
      login(data)
      navigate('/student')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-card">
      <div className="brand">Topic Recommender</div>
      <h1>Student Sign Up</h1>
      <p className="muted">Teacher accounts are provisioned separately and log in from the same Log In page.</p>
      <form onSubmit={handleSubmit}>
        <label>Full Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} required />
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Password</label>
        <input
          type="password"
          minLength={6}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">Sign Up</button>
      </form>
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  )
}
