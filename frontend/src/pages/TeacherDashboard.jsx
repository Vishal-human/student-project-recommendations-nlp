import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar.jsx'
import { getStudents, getTeacherDashboard } from '../api.js'
import { useAuth } from '../context/AuthContext.jsx'

export default function TeacherDashboard() {
  const { auth } = useAuth()
  const [data, setData] = useState(null)
  const [students, setStudents] = useState([])

  useEffect(() => {
    getTeacherDashboard().then(setData).catch(() => {})
    getStudents().then(setStudents).catch(() => {})
  }, [])

  return (
    <div>
      <Navbar />
      <div className="page">
        <h1>Welcome, {auth?.name}</h1>

        <div className="stat-grid">
          <div className="stat-card">
            <span className="stat-label">Registered Students</span>
            <span className="stat-value">{data?.registered_students ?? '—'}</span>
          </div>
        </div>

        <div className="card">
          <h2>Registered Students</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.email}</td>
                  <td>{new Date(s.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
              {students.length === 0 && (
                <tr>
                  <td colSpan={3} className="muted">
                    No students registered yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
