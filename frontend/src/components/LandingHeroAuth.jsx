import React, { useState } from 'react';
import { Sparkles, CheckCircle2, ShieldCheck, Target, FileText, ArrowRight, Eye, EyeOff, Loader2, LogIn, UserPlus } from 'lucide-react';
import axios from 'axios';

function LandingHeroAuth({ onAuthSuccess }) {
  const [isLoginView, setIsLoginView] = useState(true);
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const endpoint = isLoginView 
      ? 'http://127.0.0.1:5000/api/auth/login' 
      : 'http://127.0.0.1:5000/api/auth/register';

    const payload = isLoginView 
      ? { email: email.trim(), password: password.trim() }
      : { email: email.trim(), password: password.trim(), full_name: fullName.trim() };

    try {
      const response = await axios.post(endpoint, payload);
      const { token, user } = response.data;

      localStorage.setItem('ats_token', token);
      localStorage.setItem('ats_user', JSON.stringify(user));

      onAuthSuccess(user, token);
    } catch (err) {
      setError(err.response?.data?.error || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="landing-page-wrapper">
      {/* Top Navbar Header */}
      <header className="landing-navbar">
        <div className="nav-brand">
          <div className="brand-mark"><Sparkles size={18} /></div>
          <span className="brand-name">ReAn AI</span>
        </div>
        <div className="nav-auth-status">
          <span className="private-badge"><ShieldCheck size={14} /> 100% Private & Secure</span>
        </div>
      </header>

      {/* Main Split Grid Section */}
      <div className="landing-hero-grid">
        {/* Left Side: Product Prototype Preview & Quotation */}
        <div className="landing-left-hero">
          <div className="hero-quote-badge">
            <Sparkles size={14} /> Next-Gen Resume Intelligence Platform
          </div>

          <h1 className="hero-headline">
            Beat Corporate Recruiter Filters with <span>AI-Powered ATS Precision.</span>
          </h1>

          <blockquote className="hero-quote-box">
            <p>
              “88% of tech resumes are rejected by automated ATS parsers due to multi-column layout errors or missing technical keywords. Our Diagnostic Engine scans, repairs, and optimizes your resume for instant recruiter matches.”
            </p>
          </blockquote>

          {/* Value Prop Badges */}
          <div className="hero-features-list">
            <div className="feature-item">
              <CheckCircle2 size={16} className="feature-icon" />
              <span><strong>3-Pillar Scoring:</strong> Keyword coverage, format readability & word density analysis.</span>
            </div>
            <div className="feature-item">
              <CheckCircle2 size={16} className="feature-icon" />
              <span><strong>Mirror Parser Engine:</strong> Eliminates multi-column layout bleeding & PDF alerts.</span>
            </div>
            <div className="feature-item">
              <CheckCircle2 size={16} className="feature-icon" />
              <span><strong>1-Click Executive PDF:</strong> Auto-inserts missing skills into a clean single-column PDF.</span>
            </div>
          </div>

          {/* Interactive Prototype Preview Mockup */}
          <div className="app-prototype-card">
            <div className="prototype-header">
              <span className="proto-dot red"></span>
              <span className="proto-dot yellow"></span>
              <span className="proto-dot green"></span>
              <span className="proto-title">Live Application Prototype Preview</span>
            </div>
            <div className="prototype-body">
              <div className="proto-score-ring">
                <div className="proto-score-value">88</div>
                <div className="proto-score-label">ATS Match Score</div>
              </div>
              <div className="proto-keywords-preview">
                <span className="proto-tag match">✓ Python</span>
                <span className="proto-tag match">✓ SQL</span>
                <span className="proto-tag match">✓ Pandas</span>
                <span className="proto-tag match">✓ Tableau</span>
                <span className="proto-tag missing">+ Data Cleaning</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Inline Login & Sign Up Card */}
        <div className="landing-right-auth">
          <div className="auth-card-hero">
            <div className="auth-card-title">
              <h2>{isLoginView ? 'Log In to Your Account' : 'Create Your Account'}</h2>
              <p>{isLoginView ? 'Access your private workspace and saved ATS scan reports.' : 'Start analyzing your resumes with private account data storage.'}</p>
            </div>

            {/* Toggle Tabs */}
            <div className="auth-hero-tabs">
              <button 
                type="button"
                className={`auth-hero-tab ${isLoginView ? 'active' : ''}`}
                onClick={() => { setIsLoginView(true); setError(null); }}
              >
                <LogIn size={15} /> Log In
              </button>
              <button 
                type="button"
                className={`auth-hero-tab ${!isLoginView ? 'active' : ''}`}
                onClick={() => { setIsLoginView(false); setError(null); }}
              >
                <UserPlus size={15} /> Sign Up
              </button>
            </div>

            {error && <div className="hero-error-banner">{error}</div>}

            {/* Form */}
            <form onSubmit={handleSubmit} className="hero-auth-form">
              {!isLoginView && (
                <div className="hero-form-group">
                  <label>Full Name</label>
                  <input 
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter your full name..."
                    required
                  />
                </div>
              )}

              <div className="hero-form-group">
                <label>Email Address</label>
                <input 
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@domain.com"
                  required
                />
              </div>

              <div className="hero-form-group">
                <label>Password</label>
                <div className="password-input-wrap">
                  <input 
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                  <button 
                    type="button"
                    className="pwd-toggle-btn"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <button type="submit" className="hero-submit-btn" disabled={loading}>
                {loading ? <Loader2 className="animate-spin" size={18} /> : isLoginView ? <LogIn size={18} /> : <UserPlus size={18} />}
                {loading ? 'Authenticating…' : isLoginView ? 'Log In & Access Application' : 'Create Free Account & Access App'}
                {!loading && <ArrowRight size={18} />}
              </button>
            </form>

            <div className="hero-form-footer">
              {isLoginView ? (
                <p>Don't have an account yet? <span onClick={() => setIsLoginView(false)}>Sign up for free</span></p>
              ) : (
                <p>Already have an account? <span onClick={() => setIsLoginView(true)}>Log in to your workspace</span></p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingHeroAuth;
