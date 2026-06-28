import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

import { AuthProvider } from './context/AuthContext'
import { GoogleOAuthProvider } from '@react-oauth/google'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>

    <GoogleOAuthProvider clientId="94971980015-13ga5a3ons64j2p6gmpubejtqt5q1dkb.apps.googleusercontent.com">

      <AuthProvider>

        <App />

      </AuthProvider>

    </GoogleOAuthProvider>

  </React.StrictMode>
)