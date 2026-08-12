import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar({ title }) {
  const { auth, logout } = useAuth()

  return (
    <nav className="navbar">
      <div className="navbar-brand">Topic Recommender</div>
      <div className="navbar-right">
        <span className="navbar-user">
          {auth?.name} <span className="role-badge">{auth?.role}</span>
        </span>
        <button className="btn-secondary" onClick={logout}>
          Log Out
        </button>
      </div>
    </nav>
  )
}
