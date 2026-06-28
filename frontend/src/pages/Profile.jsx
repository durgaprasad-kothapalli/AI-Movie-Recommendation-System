import { getWatchlist } from '../services/api'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Profile() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [watchlist, setWatchlist] = useState([])
  const [ratings, setRatings] = useState([])
  const [loading, setLoading] = useState(true)



  useEffect(() => {

    const loadProfile = async () => {

      try {

        const googleUser = JSON.parse(
          localStorage.getItem('google_user')
        )

        const wRes = await getWatchlist(
          googleUser.email
        )

        setWatchlist(wRes.data.watchlist || [])

      } catch (err) {

        console.log(err)

      } finally {

        setLoading(false)
      }
    }

    loadProfile()

  }, [])


  const avgRating = ratings.length
    ? (ratings.reduce((s, r) => s + r.rating, 0) / ratings.length).toFixed(1)
    : '—'

  const handleLogout = () => { logout(); navigate('/') }

  if (loading) return <LoadingSpinner />

  return (
    <div className="page-padding">
      {/* Profile Header */}
      <div className="profile-header">
        <img
          src={
            JSON.parse(localStorage.getItem('google_user'))?.picture
            || 'https://i.pravatar.cc/100'
          }
          alt="profile"
          style={{
            width: '90px',
            height: '90px',
            borderRadius: '50%'
          }}
        />        <div>
          <div className="profile-name">{user?.username}</div>
          <div className="profile-email">{user?.email}</div>
        </div>
        <button className="btn btn-secondary" style={{ marginLeft: 'auto' }} onClick={handleLogout} id="profile-logout">
          Logout
        </button>
      </div>

      {/* Stats */}
      <h2 className="section-title" style={{ marginBottom: 20 }}>📊 Your Stats</h2>
      <div className="stats-grid" style={{ marginBottom: 40 }}>
        <div className="stat-card">
          <div className="stat-number">{watchlist.length}</div>
          <div className="stat-label">Movies in Watchlist</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{ratings.length}</div>
          <div className="stat-label">Movies Rated</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{avgRating}</div>
          <div className="stat-label">Average Rating Given</div>
        </div>
      </div>

      {/* Rating history */}
      {ratings.length > 0 && (
        <>
          <h2 className="section-title" style={{ marginBottom: 20 }}>⭐ Your Ratings</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {ratings.slice(0, 10).map((r, i) => (
              <div key={i} style={{
                background: 'var(--bg-card)', border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)', padding: '14px 20px',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
              }}>
                <span style={{ color: 'var(--text-secondary)' }}>Movie #{r.movie_id}</span>
                <span style={{ color: '#f59e0b', fontWeight: 700 }}>{'★'.repeat(Math.round(r.rating))} {r.rating}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
