import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({ baseURL: BASE })

// Attach JWT to every request if present
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('cineai_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// ── Auth ─────────────────────────────────────────────────────────────────────
export const registerUser = (data) => api.post('/register', data)
export const loginUser = (data) => api.post('/login', data)

// ── Movies ───────────────────────────────────────────────────────────────────
export const fetchMovies = (params) => api.get('/movies', { params })
export const fetchMovie = (id) => api.get(`/movie/${id}`)
export const searchMovies = (q) => api.get('/movies/search', { params: { q } })
export const fetchGenres = () => api.get('/movies/genres')

// ── Recommendations ───────────────────────────────────────────────────────────
export const fetchRecommendations = (movieId, userId, method = 'hybrid') =>
  api.get(`/recommend/${movieId}`, { params: { user_id: userId, method } })

// ── Ratings ───────────────────────────────────────────────────────────────────
export const rateMovie = (data) => api.post('/rate', data)
export const fetchRatings = (movieId) => api.get(`/ratings/${movieId}`)
export const fetchUserRatings = () => api.get('/ratings/user')

// ── Watchlist ─────────────────────────────────────────────────────────────────
export const addToWatchlist = (data) =>
  api.post('/watchlist/add', data)

export const getWatchlist = (user) =>
  api.get(`/watchlist/${user}`)

export const googleLogin = (data) =>
  api.post('/google-login', data)