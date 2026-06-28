import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar          from './components/Navbar'
import ProtectedRoute  from './components/ProtectedRoute'
import Home            from './pages/Home'
import Login           from './pages/Login'
import Register        from './pages/Register'
import MovieDetail     from './pages/MovieDetail'
import Search          from './pages/Search'
import Recommendations from './pages/Recommendations'
import Watchlist       from './pages/Watchlist'
import Profile         from './pages/Profile'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/"               element={<Home />} />
          <Route path="/login"          element={<Login />} />
          <Route path="/register"       element={<Register />} />
          <Route path="/search"         element={<Search />} />
          <Route path="/movie/:id"      element={<MovieDetail />} />
          <Route path="/recommendations/:id" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
          <Route path="/watchlist"      element={<ProtectedRoute><Watchlist /></ProtectedRoute>} />
          <Route path="/profile"        element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
