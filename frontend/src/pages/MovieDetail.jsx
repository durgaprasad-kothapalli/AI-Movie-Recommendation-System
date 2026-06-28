import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchMovie, fetchRatings, rateMovie, addToWatchlist } from '../services/api'
import { useAuth } from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import MovieCard from '../components/MovieCard'

export default function MovieDetail() {
  const { id }   = useParams()
  const navigate = useNavigate()
  const { isLoggedIn, user } = useAuth()

  const [movie, setMovie]     = useState(null)
  const [ratings, setRatings] = useState({ average: 0, count: 0 })
  const [userRating, setUserRating] = useState(0)
  const [hovered, setHovered]       = useState(0)
  const [loading, setLoading]       = useState(true)
  const [msg, setMsg]               = useState('')

  useEffect(() => {
    setLoading(true)
    Promise.all([fetchMovie(id), fetchRatings(id)])
      .then(([mRes, rRes]) => {
        setMovie(mRes.data)
        setRatings({ average: rRes.data.average, count: rRes.data.count })
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id])

  const submitRating = async (star) => {
    if (!isLoggedIn) { 
      navigate('/login');
       return }
    setUserRating(star)
    try {
await rateMovie({
  user: user?.username || 'google_user',
  movie_id: Number(id),
  rating: star
})     
 const rRes = await fetchRatings(id)
      setRatings({ average: rRes.data.average, count: rRes.data.count })
      setMsg('Rating saved! ✓')
      setTimeout(() => setMsg(''), 2500)
    } catch { setMsg('Failed to save rating.') }
  }

  const handleWatchlist = async () => {

  if (!isLoggedIn) {
    navigate('/login')
    return
  }

  try {

    const googleUser = JSON.parse(
      localStorage.getItem('google_user')
    )

    await addToWatchlist({
      user: googleUser.email,
      movie: movie
    })

    setMsg('Added to Watchlist! ✓')

    setTimeout(() => {
      setMsg('')
    }, 2500)

  } catch (err) {

    console.log(err)
    setMsg('Failed to add.')

  }
}

  if (loading) return <LoadingSpinner />
  if (!movie)  return null

  const genres = movie.genres?.split('|') || []

  return (
    <div>
      <div className="movie-detail-hero">
        {/* Poster */}
        <div className="movie-detail-poster">
          <img src={movie.poster_url || 'https://dummyimage.com/300x450/1e293b/ffffff&text=No+Poster'}
            alt={movie.title}
            onError={e => { e.target.src = 'https://dummyimage.com/300x450/1e293b/ffffff&text=No+Poster' }} />
        </div>

        {/* Info */}
        <div className="movie-detail-info">
          {msg && <div className="alert alert-success">{msg}</div>}

          <h1 className="movie-detail-title">{movie.title}</h1>

          <div className="movie-badges">
            {genres.map(g => <span key={g} className="badge badge-accent">{g}</span>)}
            {movie.release_year && movie.release_year !== 'N/A' &&
              <span className="badge">{movie.release_year}</span>}
          </div>

          <p className="movie-description">{movie.description}</p>

          {/* Average Rating */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ color: '#f59e0b', fontSize: '1.2rem' }}>⭐ {ratings.average.toFixed(1)}</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>({ratings.count} ratings)</span>
          </div>

          {/* Star Rating */}
          <div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 8 }}>
              {isLoggedIn ? 'Your Rating:' : 'Log in to rate'}
            </p>
            <div className="star-rating" id="star-rating-group">
              {[1,2,3,4,5].map(s => (
                <span key={s} className={`star ${(hovered || userRating) >= s ? 'active' : ''}`}
                  onMouseEnter={() => setHovered(s)}
                  onMouseLeave={() => setHovered(0)}
                  onClick={() => submitRating(s)}
                  id={`star-${s}`}
                >★</span>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <button id="add-watchlist-btn" className="btn btn-primary" onClick={handleWatchlist}>
              📌 Add to Watchlist
            </button>
            <Link to={`/recommendations/${id}`} className="btn btn-secondary">
              🤖 Get Recommendations
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
