import { googleLogin } from '../services/api'
import { GoogleLogin } from '@react-oauth/google'
import { jwtDecode } from 'jwt-decode'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { loginUser } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Login() {

  const [form, setForm] = useState({
    email: '',
    password: ''
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  const handleChange = e => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async e => {

    e.preventDefault()

    setError('')
    setLoading(true)

    try {

      const res = await loginUser(form)

      login(res.data.user, res.data.token)

      navigate('/')

    } catch (err) {

      setError(
        err.response?.data?.error ||
        'Login failed. Please try again.'
      )

    } finally {

      setLoading(false)
    }
  }

  return (

    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          🎬 CineAI
        </div>

        <h2>Welcome Back</h2>

        <p className="auth-subtitle">
          Sign in to get personalised recommendations
        </p>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} id="login-form">

          <div className="form-group">

            <label
              className="form-label"
              htmlFor="login-email"
            >
              Email Address
            </label>

            <input
              id="login-email"
              name="email"
              type="email"
              className="form-input"
              placeholder="you@example.com"
              value={form.email}
              onChange={handleChange}
              required
            />

          </div>

          <div className="form-group">

            <label
              className="form-label"
              htmlFor="login-password"
            >
              Password
            </label>

            <input
              id="login-password"
              name="password"
              type="password"
              className="form-input"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              required
            />

          </div>

          <button
            id="login-submit"
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Signing in…' : 'Sign In'}
          </button>

        </form>
        <div
          style={{
            marginTop: '20px',
            display: 'flex',
            justifyContent: 'center'
          }}
        >

          <GoogleLogin

            onSuccess={async (credentialResponse) => {

  const user = jwtDecode(
    credentialResponse.credential
  )

  try {

    const res = await googleLogin({
      email: user.email,
      name: user.name,
      picture: user.picture
    })

login(res.data.user, res.data.token)

localStorage.setItem(
  'google_user',
  JSON.stringify(res.data.user)
)

alert('Google Login Success')

navigate('/')

  } catch (err) {

    console.log(err)

    alert('Google Login Failed')
  }
}}
          />

        </div>


        <div className="auth-footer">

          Don't have an account?

          <Link to="/register">
            Create one
          </Link>

        </div>

      </div>

    </div>
  )
}