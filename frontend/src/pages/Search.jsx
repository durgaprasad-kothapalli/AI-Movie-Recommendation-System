import { useEffect, useState, useCallback } from 'react'
import { fetchMovies, fetchGenres } from '../services/api'
import MovieCard from '../components/MovieCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Search() {
  const [query, setQuery]   = useState('')
  const [genre, setGenre]   = useState('')
  const [genres, setGenres] = useState([])
  const [movies, setMovies] = useState([])
  const [total, setTotal]   = useState(0)
  const [page, setPage]     = useState(1)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchGenres().then(r => setGenres(r.data.genres || [])).catch(() => {})
  }, [])

  const load = useCallback(async (q, g, p) => {
    setLoading(true)
    try {
      const res = await fetchMovies({ q, genre: g, page: p, limit: 20 })
      if (p === 1) setMovies(res.data.movies || [])
      else setMovies(prev => [...prev, ...(res.data.movies || [])])
      setTotal(res.data.total || 0)
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { setPage(1); load(query, genre, 1) }, [query, genre])

  const loadMore = () => { const next = page + 1; setPage(next); load(query, genre, next) }

  return (
    <div className="page-padding">
      <h1 className="section-title" style={{ fontSize: '2rem', marginBottom: 28 }}>🎬 Browse Movies</h1>

      {/* Search input */}
      <div className="search-wrapper" style={{ maxWidth: '100%', marginBottom: 24 }}>
        <span className="search-icon">🔍</span>
        <input
          id="search-page-input"
          className="search-input"
          placeholder="Search by title…"
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>

      {/* Genre filter */}
      <div className="genre-filter" id="genre-filter">
        <button className={`genre-chip ${!genre ? 'active' : ''}`} onClick={() => setGenre('')}>All</button>
        {genres.map(g => (
          <button key={g} id={`genre-${g}`} className={`genre-chip ${genre === g ? 'active' : ''}`}
            onClick={() => setGenre(g === genre ? '' : g)}>{g}</button>
        ))}
      </div>

      {/* Results count */}
      <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: 20 }}>
        {total} movie{total !== 1 ? 's' : ''} found
      </p>

      {loading && movies.length === 0 ? <LoadingSpinner /> : (
        <>
          {movies.length === 0 ? (
            <div className="empty-state">
              <div className="icon">🎭</div>
              <h3>No movies found</h3>
              <p>Try a different search or genre filter.</p>
            </div>
          ) : (
            <div className="movies-grid">
              {movies.map(m => <MovieCard key={m.movieId} movie={m} />)}
            </div>
          )}

          {movies.length < total && (
            <div style={{ textAlign: 'center', marginTop: 40 }}>
              <button id="load-more-btn" className="btn btn-secondary" onClick={loadMore} disabled={loading}>
                {loading ? 'Loading…' : 'Load More'}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
