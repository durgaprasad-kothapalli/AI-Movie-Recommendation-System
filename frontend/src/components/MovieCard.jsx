import { useNavigate } from 'react-router-dom'

export default function MovieCard({ movie, showScore = false }) {

  const navigate = useNavigate()

  const genres =
    movie.genres?.split('|').slice(0, 2).join(', ') || ''

  return (

    <div
      className="movie-card"
      id={`movie-card-${movie.movieId}`}
      onClick={() => navigate(`/movie/${movie.movieId}`)}
      role="button"
      aria-label={`View ${movie.title}`}
    >

      <div className="movie-card-poster">

<img
  src={
    movie.poster_url ||
    "https://placehold.co/300x450/1e293b/ffffff?text=No+Poster"
  }
  alt={movie.title}
  loading="lazy"
/>

        <div className="movie-card-overlay">

          <span
            style={{
              color: '#fff',
              fontSize: '0.85rem',
              fontWeight: 600
            }}
          >
            View Details →
          </span>

        </div>

        {showScore && movie.score && (

          <div className="movie-card-score">
            ⭐ {(movie.score * 5).toFixed(1)}
          </div>

        )}

      </div>

      <div className="movie-card-body">

        <div className="movie-card-title">
          {movie.title}
        </div>

        <div className="movie-card-genre">
          {genres}
        </div>

      </div>

    </div>
  )
}