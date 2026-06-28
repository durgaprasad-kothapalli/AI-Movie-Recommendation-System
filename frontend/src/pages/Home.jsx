import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchMovies } from '../services/api'
import MovieCard from '../components/MovieCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Home() {
  const [movies, setMovies]   = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMovies({ limit: 30 })
      .then(r => setMovies(r.data.movies || []))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const trending  = movies.slice(0, 10)
  const action    = movies.filter(m => m.genres?.includes('Action')).slice(0, 10)
  const drama     = movies.filter(m => m.genres?.includes('Drama')).slice(0, 10)

  return (
    <div>
      {/* Hero */}
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-badge">✨ AI-Powered Recommendations</div>
          <h1>Discover Movies You'll <span>Actually Love</span></h1>
          <p>Our hybrid AI engine analyses your taste and surfaces the perfect films — blending content similarity with what viewers like you enjoy most.</p>
          <div className="hero-actions">
            <Link to="/search" className="btn btn-primary">🎬 Browse Movies</Link>
            <Link to="/register" className="btn btn-secondary">Create Free Account</Link>
          </div>
        </div>
      </section>

      <div className="page-padding">
        {loading ? <LoadingSpinner /> : (
          <>
            <section style={{ marginBottom: 48 }}>
              <h2 className="section-title">🔥 Trending Now</h2>
              <div className="movies-grid">
                {trending.map(m => <MovieCard key={m.movieId} movie={m} />)}
              </div>
            </section>

            {action.length > 0 && (
              <section style={{ marginBottom: 48 }}>
                <h2 className="section-title">⚡ Action & Adventure</h2>
                <div className="movies-grid">
                  {action.map(m => <MovieCard key={m.movieId} movie={m} />)}
                </div>
              </section>
            )}

            {drama.length > 0 && (
              <section>
                <h2 className="section-title">🎭 Drama Highlights</h2>
                <div className="movies-grid">
                  {drama.map(m => <MovieCard key={m.movieId} movie={m} />)}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </div>
  )
}
