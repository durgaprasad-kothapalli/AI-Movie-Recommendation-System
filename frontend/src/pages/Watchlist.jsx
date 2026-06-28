import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getWatchlist } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Watchlist() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {

    const loadWatchlist = async () => {

      console.log("WATCHLIST LOADING")

      try {

        setLoading(true)

        const googleUser = JSON.parse(
          localStorage.getItem('google_user')
        )

        console.log("API CALL")
        const res = await getWatchlist(
          
          googleUser.email
        )
       console.log(res.data.watchlist)

        setItems(res.data.watchlist || [])

      } catch (err) {

        console.log(err)
        setItems([])

      } finally {

        setLoading(false)
      }
    }

    loadWatchlist()

  }, [])




  if (loading) return <LoadingSpinner />

  return (
    <div className="page-padding">
      <h1 className="section-title" style={{ fontSize: '2rem', marginBottom: 28 }}>
        📌 My Watchlist
      </h1>

      {items.length === 0 ? (
        <div className="empty-state">
          <div className="icon">📋</div>
          <h3>Your watchlist is empty</h3>
          <p>Browse movies and click "Add to Watchlist" to save them here.</p>
          <Link to="/search" className="btn btn-primary" style={{ marginTop: 20 }}>Browse Movies</Link>
        </div>
      ) : (
        <div className="watchlist-grid">
          {items.map(item => (
            <div key={item.movieId} className="watchlist-card" id={`watchlist-${item.movieId}`}>
              <img
src={item.poster_path || item.poster_url || 'https://dummyimage.com/300x450/1e293b/ffffff&text=No+Poster'}                alt={item.title}
                style={{ aspectRatio: '2/3', objectFit: 'cover' }}
                onError={e => { e.target.src = 'https://dummyimage.com/300x450/1e293b/ffffff&text=No+Poster' }}
              />
              <div className="watchlist-card-body">
                <div className="title">{item.title}</div>
                <div className="genre">{item.genres?.split('|').slice(0, 2).join(', ')}</div>
              </div>
              <div className="watchlist-card-actions">
                <Link to={`/movie/${item.movieId}`} className="btn btn-secondary btn-sm" style={{ flex: 1, textAlign: 'center' }}>
                  View
                </Link>
                <Link to={`/recommendations/${item.movieId}`} className="btn btn-primary btn-sm" style={{ flex: 1, textAlign: 'center' }}>
                  Similar
                </Link>

              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
