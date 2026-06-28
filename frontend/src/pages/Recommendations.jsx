import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchRecommendations, fetchMovie } from '../services/api'
import { useAuth } from '../context/AuthContext'
import MovieCard from '../components/MovieCard'
import LoadingSpinner from '../components/LoadingSpinner'

const METHODS = [
  { key: 'hybrid',        label: '🔀 Hybrid',        desc: 'Best of both algorithms' },
  { key: 'content',       label: '🎬 Content-Based', desc: 'Based on movie features' },
  { key: 'collaborative', label: '👥 Collaborative',  desc: 'Based on user taste' },
]

export default function Recommendations() {
  const { id }   = useParams()
  const { user } = useAuth()
  const [movie, setMovie]         = useState(null)
  const [method, setMethod] = useState('content')
  const [movies, setMovies]       = useState([])
  const [loading, setLoading]     = useState(false)

  useEffect(() => {
    fetchMovie(id).then(r => setMovie(r.data)).catch(() => {})
  }, [id])

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetchRecommendations(id, user?.user_id, method)
      .then(r => setMovies(r.data.recommendations || []))
      .catch(() => setMovies([]))
      .finally(() => setLoading(false))
  }, [id, method])

  return (
    <div className="page-padding">
      {movie && (
        <div style={{ marginBottom: 32 }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: 8 }}>
            Because you liked…
          </p>
          <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>🤖 Recommendations for <span style={{ color: 'var(--accent-light)' }}>{movie.title}</span></h1>
        </div>
      )}

      {/* Method selector */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 32, flexWrap: 'wrap' }} id="method-selector">
        {METHODS.map(m => (
          <button
            key={m.key}
            id={`method-${m.key}`}
            onClick={() => setMethod(m.key)}
            className="btn"
            style={{
              background: method === m.key ? 'var(--accent)' : 'var(--bg-glass)',
              border: `1px solid ${method === m.key ? 'var(--accent)' : 'var(--border)'}`,
              color: method === m.key ? '#fff' : 'var(--text-secondary)',
              flexDirection: 'column', gap: 2, padding: '10px 20px',
            }}
          >
            <span style={{ fontWeight: 700 }}>{m.label}</span>
            <span style={{ fontSize: '0.72rem', opacity: 0.8 }}>{m.desc}</span>
          </button>
        ))}
      </div>

      {loading ? <LoadingSpinner /> : (
        movies.length === 0 ? (
          <div className="empty-state">
            <div className="icon">🤔</div>
            <h3>No recommendations found</h3>
            <p>Try a different method or rate more movies.</p>
          </div>
        ) : (
          <div className="movies-grid">
            {movies.map(m => <MovieCard key={m.movieId} movie={m} showScore />)}
          </div>
        )
      )}
    </div>
  )
}
