import { useState, useEffect, useRef } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          ×
        </button>

        <h2 className="modal-title">{title}</h2>

        {children}
      </div>
    </div>
  );
}

function App() {
  const [showSignup, setShowSignup] = useState(false);
  const [showLogin, setShowLogin] = useState(false);

  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {});
    }
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/ask?question=${encodeURIComponent(query)}`
      );

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setResult({
        answer: "Unable to connect to backend.",
        route: "error",
        retrieval: false,
        fallback: false,
        sources: [],
      });
    }

    setLoading(false);
  };

  return (
    <div className="app">

      {/* Background */}

      <div className="video-container">
        <video
          ref={videoRef}
          className="video-bg"
          src="/heart-bg.mp4"
          autoPlay
          muted
          loop
          playsInline
        />

        <div className="video-overlay" />
        <div className="hud-grid" />
        <div className="scan-line" />
      </div>

      {/* Floating Particles */}

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
            <a href="#">Features</a>
            <a href="#">About</a>
            <a href="#">Research</a>
          </div>
        </div>

        <div className="nav-right">
          <button
            className="btn-signup"
            onClick={() => setShowSignup(true)}
          >
            Sign Up
          </button>

          <button
            className="btn-login"
            onClick={() => setShowLogin(true)}
          >
            Login
          </button>
        </div>
      </nav>

      {/* Hero */}

      <main className="hero">

        <div className="hero-content">

          <p className="tagline">
            AI-POWERED MEDICAL RESEARCH
          </p>

          <h1 className="hero-title">
            Precision built into
            <br />
            every diagnosis.
          </h1>

          <p className="hero-subtitle">
            Hybrid AI architecture. Sensitive medical data stays local.
            Advanced reasoning uses Gemini.
          </p>

          {/* Search */}

          <form onSubmit={handleSearch} className="search-form">

            <div className="search-wrapper">

              <span className="search-icon">🔍</span>

              <input
                className="search-input"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a medical research question..."
              />

              <button
                className="search-btn"
                disabled={loading}
              >
                {loading ? "⏳" : "⚡"}
              </button>

            </div>

          </form>

          {/* Results */}

          {result && (

            <div className="result-card">

              <div className={`route-badge ${result.route}`}>

                {result.route === "local"
                  ? "🛡️ Local Ollama"
                  : result.route === "cloud"
                  ? "☁️ Gemini"
                  : "❌ Error"}

              </div>

              {result.retrieval && (
                <div className="retrieval-badge">
                   Answer generated using indexed research papers.
                </div>
              )}

              {result.fallback && (
                <div className="fallback-badge">
                   No relevant paper found. Using general medical knowledge.
                </div>
              )}

              <div className="answer-text">
                {result.answer}
              </div>

              {result.sources?.length > 0 && (

                <div className="sources">

                  <h3> Supporting Research Papers</h3>

                  {result.sources.map((paper, index) => (

                    <div
                      key={index}
                      className="source-card"
                    >

                      <h4>{paper.title}</h4>

                      <p>
                        <strong>Authors:</strong>{" "}
                        {paper.authors || "Unknown"}
                      </p>

                      <p>
                        <strong>Journal:</strong>{" "}
                        {paper.journal || "Unknown"}
                      </p>

                      <p>
                        <strong>Year:</strong>{" "}
                        {paper.year}
                      </p>

                      <p>
                        <strong>PMC ID:</strong>{" "}
                        {paper.pmc_id}
                      </p>

                      {paper.url && (
                        <a
                          href={paper.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          🔗 Read Full Paper
                        </a>
                      )}

                    </div>

                  ))}

                </div>

              )}

            </div>

          )}

          {/* Stats */}

          <div className="hero-stats">

            <div className="stat">
              <span className="stat-num">64K+</span>
              <span className="stat-label">Research Chunks</span>
            </div>

            <div className="stat">
              <span className="stat-num">440+</span>
              <span className="stat-label">Medical Papers</span>
            </div>

            <div className="stat">
              <span className="stat-num">AI</span>
              <span className="stat-label">Hybrid RAG</span>
            </div>

          </div>

        </div>

      </main>

      {/* Footer */}

      <footer className="footer">
        <p>
          Local LLM • Ollama • Gemini • ChromaDB • Evidence-based Medical AI
        </p>
      </footer>

      {/* Signup */}

      <Modal
        isOpen={showSignup}
        onClose={() => setShowSignup(false)}
        title="Sign Up"
      >
        <form
          className="auth-form"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            className="auth-input"
            placeholder="Full Name"
          />

          <input
            className="auth-input"
            placeholder="Email"
          />

          <input
            className="auth-input"
            type="password"
            placeholder="Password"
          />

          <button className="auth-btn">
            Create Account
          </button>
        </form>
      </Modal>

      {/* Login */}

      <Modal
        isOpen={showLogin}
        onClose={() => setShowLogin(false)}
        title="Login"
      >
        <form
          className="auth-form"
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            className="auth-input"
            placeholder="Email"
          />

          <input
            className="auth-input"
            type="password"
            placeholder="Password"
          />

          <button className="auth-btn">
            Login
          </button>
        </form>
      </Modal>

    </div>
  );
}


export default App;