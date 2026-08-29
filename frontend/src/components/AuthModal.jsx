import React, { useState } from 'react';
import { X, Lock, Mail, User, Eye, EyeOff, Loader2, LogIn, UserPlus } from 'lucide-react';
import axios from 'axios';

function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isLoginView, setIsLoginView] = useState(true);
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

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
      onClose();
    } catch (err) {
      setError(err.response?.data?.error || 'Authentication failed. Please check your details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="auth-modal-card">
        <button className="close-modal-btn" onClick={onClose} aria-label="Close modal">
          <X size={18} />
        </button>

        <div className="auth-modal-header">
          <h2>{isLoginView ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{isLoginView ? 'Log in to access your saved resume scans and ATS reports.' : 'Sign up to automatically save your resume scans and track ATS scores.'}</p>
        </div>

        <div className="auth-tab-row">
          <button 
            className={`auth-tab ${isLoginView ? 'active' : ''}`}
            onClick={() => { setIsLoginView(true); setError(null); }}
          >
            <LogIn size={15} /> Log In
          </button>
          <button 
            className={`auth-tab ${!isLoginView ? 'active' : ''}`}
            onClick={() => { setIsLoginView(false); setError(null); }}
          >
            <UserPlus size={15} /> Sign Up
          </button>
        </div>

        {error && <div className="auth-error-card">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          {!isLoginView && (
            <div className="form-group">
              <label>Full Name</label>
              <div className="input-with-icon">
                <User size={16} className="input-icon" />
                <input 
                  type="text" 
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Enter your full name..."
                  required
                />
              </div>
            </div>
          )}

          <div className="form-group">
            <label>Email Address</label>
            <div className="input-with-icon">
              <Mail size={16} className="input-icon" />
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@domain.com"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-with-icon">
              <Lock size={16} className="input-icon" />
              <input 
                type={showPassword ? 'text' : 'password'} 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />
              <button 
                type="button" 
                className="toggle-password-btn"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button type="submit" className="auth-submit-btn" disabled={loading}>
            {loading ? <Loader2 className="animate-spin" size={18} /> : isLoginView ? <LogIn size={18} /> : <UserPlus size={18} />}
            {loading ? 'Authenticating…' : isLoginView ? 'Log In to Your Account' : 'Create Free Account'}
          </button>
        </form>

        <div className="auth-modal-footer">
          {isLoginView ? (
            <p>Don't have an account? <span onClick={() => setIsLoginView(false)}>Sign up now</span></p>
          ) : (
            <p>Already have an account? <span onClick={() => setIsLoginView(true)}>Log in here</span></p>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthModal;
