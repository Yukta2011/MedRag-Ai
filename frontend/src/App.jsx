import { useState, useEffect, useRef } from 'react'
import './App.css'

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <h2 className="modal-title">{title}</h2>
        {children}
      </div>
    </div>
  )
}

function App() {
  const [showSignup, setShowSignup] = useState(false)
  const [showLogin, setShowLogin] = useState(false)
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const videoRef = useRef(null)

  // Auto-play video on load
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {})
    }
  }, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/ask?question=${encodeURIComponent(query)}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setResult({
        answer: 'Error connecting to backend. Make sure FastAPI is running.',
        sources: [],
        route: 'error',
        model_used: 'none'
      })
    }
    setLoading(false)
  }

  return (
    <div className="app">
      {/* Video Background */}
      <div className="video-container">
        <video
          ref={videoRef}
          className="video-bg"
          src="/heart-bg.mp4"
          muted
          loop
          playsInline
          autoPlay
        />
        <div className="video-overlay" />
        <div className="hud-grid" />
        <div className="scan-line" />
      </div>

      {/* Floating particles */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${5 + Math.random() * 10}s`,
            }}
          />
        ))}
      </div>

      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-left">
          <div className="logo">
            <span className="logo-icon">⚕️</span>
            <span className="logo-text">MedRAG AI</span>
          </div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#research">Research</a>
          </div>
        </div>
        <div className="nav-right">
          <button className="btn-signup" onClick={() => setShowSignup(true)}>Sign Up</button>
          <button className="btn-login" onClick={() => setShowLogin(true)}>Login</button>
        </div>
      </nav>

      {/* Hero / Search Section */}
      <main className="hero">
        <div className="hero-content">
          <p className="tagline">AI-POWERED MEDICAL RESEARCH</p>

          <h1 className="hero-title">
            Precision built into<br />
            every diagnosis.
          </h1>

          <p className="hero-subtitle">
            Hybrid AI architecture. Sensitive data stays local. 
            Complex analysis uses cloud.
          </p>

          {/* Search Box */}
          <form onSubmit={handleSearch} className="search-form">
            <div className="search-wrapper">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a medical research question..."
                className="search-input"
              />
              <button type="submit" className="search-btn" disabled={loading}>
                {loading ? '⏳' : '⚡'}
              </button>
            </div>
          </form>

          {/* Results */}
          {result && (
            <div className="result-card">
              <div className={`route-badge ${result.route}`}>
                {result.route === 'local' ? '🛡️ Local AI' : 
                 result.route === 'cloud' ? '☁️ Cloud AI' : '❌ Error'}
              </div>
              <div className="answer-text">{result.answer}</div>
              {result.sources?.length > 0 && (
                <div className="sources">
                  <h4>Sources:</h4>
                  {result.sources.map((s, i) => (
                    <div key={i} className="source-item">[{i+1}] {s}</div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Stats */}
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-num">27K+</span>
              <span className="stat-label">Medical Papers</span>
            </div>
            <div className="stat">
              <span className="stat-num">99.7%</span>
              <span className="stat-label">Accuracy</span>
            </div>
            <div className="stat">
              <span className="stat-num">0ms</span>
              <span className="stat-label">Latency</span>
            </div>
          </div>
        </div>
      </main>

      {/* HUD Data Overlay */}
      <div className="hud-data left">
        <div className="hud-item">
          <span className="hud-value">240</span>
          <span className="hud-unit">bpm</span>
        </div>
        <div className="hud-item">
          <span className="hud-value">85</span>
          <span className="hud-unit">mmHg</span>
        </div>
        <div className="hud-item">
          <span className="hud-value">42</span>
          <span className="hud-unit">L/min</span>
        </div>
      </div>

      <div className="hud-data right">
        <div className="hud-item">
          <span className="hud-value">98%</span>
          <span className="hud-unit">O2 Sat</span>
        </div>
        <div className="hud-item">
          <span className="hud-value">5.8</span>
          <span className="hud-unit">pH</span>
        </div>
        <div className="hud-item">
          <span className="hud-value">12°</span>
          <span className="hud-unit">Temp</span>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Local LLM: Mistral • Cloud: Gemini • Vector DB: ChromaDB • 27K+ Chunks</p>
      </footer>

      {/* Modals */}
      <Modal isOpen={showSignup} onClose={() => setShowSignup(false)} title="Sign Up">
        <form onSubmit={(e) => e.preventDefault()} className="auth-form">
          <input type="text" placeholder="Full Name" className="auth-input" />
          <input type="email" placeholder="Email" className="auth-input" />
          <input type="password" placeholder="Password" className="auth-input" />
          <button className="auth-btn">Create Account</button>
        </form>
      </Modal>

      <Modal isOpen={showLogin} onClose={() => setShowLogin(false)} title="Login">
        <form onSubmit={(e) => e.preventDefault()} className="auth-form">
          <input type="email" placeholder="Email" className="auth-input" />
          <input type="password" placeholder="Password" className="auth-input" />
          <button className="auth-btn">Sign In</button>
        </form>
      </Modal>
    </div>
  )
}

export default App