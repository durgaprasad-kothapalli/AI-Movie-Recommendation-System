import logo from '../assets/logo.png'
import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { searchMovies } from '../services/api'

export default function Navbar() {
  const { user, logout, isLoggedIn } = useAuth()
  const googleUser = JSON.parse(
    localStorage.getItem('google_user')
  )
  const navigate = useNavigate()
  const location = useLocation()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [showDrop, setShowDrop] = useState(false)
  const debounceRef = useRef(null)
  const dropRef = useRef(null)

  useEffect(() => {
    clearTimeout(debounceRef.current)
    if (!query.trim()) { setResults([]); setShowDrop(false); return }
    debounceRef.current = setTimeout(async () => {
      try {
        const res = await searchMovies(query)
        setResults(res.data.results || [])
        setShowDrop(true)
      } catch { setResults([]) }
    }, 300)
  }, [query])

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => { if (dropRef.current && !dropRef.current.contains(e.target)) setShowDrop(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleSelect = (id) => { setQuery(''); setShowDrop(false); navigate(`/movie/${id}`) }
  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

  return (
    <nav className="navbar">
      <div className="navbar-inner">
<Link to="/" className="navbar-logo">
  <img
    src={logo}
    alt="CineAI Logo"
    className="logo-image"
  />
</Link>

        {/* Live Search */}
        <div className="search-wrapper" ref={dropRef} style={{ flex: 1, maxWidth: 400 }}>
          <span className="search-icon">🔍</span>
          <input
            id="navbar-search"
            className="search-input"
            placeholder="Search movies…"
            value={query}
            onChange={e => setQuery(e.target.value)}
            style={{ padding: '10px 16px 10px 44px', fontSize: '0.9rem' }}
          />
          {showDrop && results.length > 0 && (
            <div className="search-dropdown">
              {results.map(m => (
                <div key={m.movieId} className="search-item" onClick={() => handleSelect(m.movieId)}>
                  <img src={m.poster_url} alt={m.title}
                    onError={e => { e.target.src = 'https://via.placeholder.com/36x54?text=?' }} />
                  <div className="search-item-info">
                    <div className="title">{m.title}</div>
                    <div className="genre">{m.genres?.split('|').slice(0, 2).join(', ')}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="navbar-links">
          <Link to="/" className={isActive('/')}><span>Home</span></Link>
          <Link to="/search" className={isActive('/search')}><span>Browse</span></Link>
          {isLoggedIn ? (
            <>
              <Link to="/watchlist" className={isActive('/watchlist')}><span>Watchlist</span></Link>
              <Link to="/profile" className={isActive('/profile')}>

                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px'
                  }}
                >

                  <img
                    src={
                      googleUser?.picture ||
                      'https://i.pravatar.cc/40'
                    }
                    alt="profile"
                    style={{
                      width: '35px',
                      height: '35px',
                      borderRadius: '50%'
                    }}
                  />

                  <span>
                    {googleUser?.name || user?.username}
                  </span>

                </div>

              </Link>
              <button className="nav-link" onClick={() => { logout(); navigate('/') }}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-btn-primary">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
