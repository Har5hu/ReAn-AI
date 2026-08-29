import { useState, useEffect } from 'react';
import axios from 'axios';
import { ArrowRight, Loader2, Sparkles, Trash2, LayoutDashboard, Target, Lightbulb, FileText, CheckCircle2, Eye, Award, Split, BookOpen, Clock, RefreshCw, Download, LogIn, UserPlus, LogOut, UserCheck, ExternalLink, ArrowLeft, RotateCcw } from 'lucide-react';
import UploadBox from './components/UploadBox';
import ATSGauge from './components/ATSGauge';
import KeywordPanel from './components/KeywordPanel';
import Suggestions from './components/Suggestions';
import ResumeChanges from './components/ResumeChanges';
import MirrorParserView from './components/MirrorParserView';
import ResumeInspector from './components/ResumeInspector';
import ResumeTemplates from './components/ResumeTemplates';
import LandingHeroAuth from './components/LandingHeroAuth';
import './index.css';

function formatDisplayRole(domain) {
  if (!domain || domain.toLowerCase() === "technical" || domain.toLowerCase() === "technical role") {
    return "Data Analyst";
  }
  return domain;
}

function App() {
  const [jobDescription, setJobDescription] = useState(() => {
    return sessionStorage.getItem('savedJobDesc') || '';
  });

  // User Auth State
  const [currentUser, setCurrentUser] = useState(() => {
    const savedUser = localStorage.getItem('ats_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  
  const [authToken, setAuthToken] = useState(() => {
    return localStorage.getItem('ats_token') || null;
  });

  const [results, setResults] = useState(() => {
    const saved = sessionStorage.getItem('savedResults');
    if (!saved) return null;
    try {
      const parsed = JSON.parse(saved);
      if (!parsed.skills_breakdown) {
        sessionStorage.removeItem('savedResults');
        return null;
      }
      return parsed;
    } catch (e) {
      sessionStorage.removeItem('savedResults');
      return null;
    }
  });

  // Persistent Account Scan History State
  const [history, setHistory] = useState(() => {
    if (!currentUser) return [];
    const userKey = `ats_user_history_${currentUser.id}`;
    const savedHistory = localStorage.getItem(userKey) || localStorage.getItem('scanHistory');
    return savedHistory ? JSON.parse(savedHistory) : [];
  });

  const [pageView, setPageView] = useState('review'); // 'review' | 'inspector' | 'templates' | 'history'
  const [activeTab, setActiveTab] = useState('skills');

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  useEffect(() => {
    sessionStorage.setItem('savedJobDesc', jobDescription);
  }, [jobDescription]);

  useEffect(() => {
    if (results) {
      sessionStorage.setItem('savedResults', JSON.stringify(results));
    } else {
      sessionStorage.removeItem('savedResults');
    }
  }, [results]);

  // Sync scan history with SQLite database & local storage backup
  useEffect(() => {
    if (authToken && currentUser) {
      const userKey = `ats_user_history_${currentUser.id}`;
      
      axios.get('http://127.0.0.1:5000/api/user/scans', {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      .then(res => {
        if (res.data.scans && res.data.scans.length > 0) {
          const formatted = res.data.scans.map(s => ({
            id: s.id,
            date: s.scan_date,
            score: s.score,
            jobDomain: formatDisplayRole(s.job_domain),
            resumeFilename: s.resume_filename || "Resume.pdf",
            results: s.results
          }));
          setHistory(formatted);
          localStorage.setItem(userKey, JSON.stringify(formatted));
          localStorage.setItem('scanHistory', JSON.stringify(formatted));
        }
      })
      .catch(err => console.log("Account scan sync notice:", err.message));
    }
  }, [authToken, currentUser]);

  const handleAuthSuccess = (user, token) => {
    setCurrentUser(user);
    setAuthToken(token);
  };

  const handleSignOut = () => {
    localStorage.removeItem('ats_token');
    localStorage.removeItem('ats_user');
    sessionStorage.removeItem('savedResults');
    setCurrentUser(null);
    setAuthToken(null);
    setResults(null);
    setHistory([]);
  };

  const handleResetScan = () => {
    setResults(null);
    setFile(null);
    setError(null);
    sessionStorage.removeItem('savedResults');
  };

  const handleSelectHistoryScanInCurrentTab = (scanItem) => {
    if (scanItem && scanItem.results) {
      setResults(scanItem.results);
      setPageView('review');
      setActiveTab('skills');
    }
  };

  const handleDeleteScan = async (scanId) => {
    if (!window.confirm("Are you sure you want to delete this scan report from your account?")) return;
    try {
      if (authToken) {
        await axios.delete(`http://127.0.0.1:5000/api/user/scans/${scanId}`, {
          headers: { Authorization: `Bearer ${authToken}` }
        });
      }
      const updated = history.filter(item => item.id !== scanId);
      setHistory(updated);
      if (currentUser) {
        localStorage.setItem(`ats_user_history_${currentUser.id}`, JSON.stringify(updated));
      }
    } catch (err) {
      console.log("Error deleting scan:", err.message);
    }
  };

  const handleGlobalDownloadPDF = async (targetResults = results) => {
    if (!targetResults) return;
    try {
      setDownloadingPDF(true);
      const missingHard = targetResults?.skills_breakdown?.missing_hard || [];
      const rawText = targetResults?.raw_extracted_text || "";

      const response = await axios.post(
        'http://127.0.0.1:5000/generate_pdf',
        {
          resume_text: rawText,
          missing_keywords: missingHard
        },
        { responseType: 'blob' }
      );

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Optimized_ATS_Resume.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Could not generate optimized PDF. Please ensure the backend server is running.");
    } finally {
      setDownloadingPDF(false);
    }
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear your scan history list?')) {
      setHistory([]);
      if (currentUser) {
        localStorage.removeItem(`ats_user_history_${currentUser.id}`);
      }
    }
  };

  const preserveJobDescriptionLayout = (value) => value
    .replace(/\r\n?/g, '\n')
    .split('\n')
    .map((line) => line.replace(/[\t\f\v ]+/g, ' ').trim())
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trimStart();

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload your resume before running the scan.');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription.trim());

    const headers = { 'Content-Type': 'multipart/form-data' };
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', formData, { headers });
      
      const detectedRole = formatDisplayRole(response.data.job_domain);
      response.data.job_domain = detectedRole;

      setResults(response.data);
      setActiveTab('skills');
      setPageView('review');

      const newHistoryItem = {
         id: response.data.saved_scan_id || Date.now(),
         date: new Date().toLocaleDateString(),
         score: response.data.overall_score,
         jobDomain: detectedRole,
         resumeFilename: file.name,
         results: response.data
      };
      
      const updatedHistory = [newHistoryItem, ...history.filter(h => h.id !== newHistoryItem.id)];
      setHistory(updatedHistory);

      if (currentUser) {
        localStorage.setItem(`ats_user_history_${currentUser.id}`, JSON.stringify(updatedHistory));
        localStorage.setItem('scanHistory', JSON.stringify(updatedHistory));
      }

    } catch (err) {
      setError(err.response?.data?.error || 'We could not analyze this resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const hasJobDescription = jobDescription.trim().length > 0;

  // IF USER IS NOT LOGGED IN: Render Landing Hero & Authentication Interface
  if (!currentUser) {
    return <LandingHeroAuth onAuthSuccess={handleAuthSuccess} />;
  }

  // IF USER IS LOGGED IN: Render Private Application Workspace
  return (
    <div className="app-shell-full">
      {/* Top Navbar */}
      <nav className="top-navbar">
        <div className="nav-brand">
          <div className="brand-mark"><Sparkles size={16} /></div>
          <span>ReAn AI</span>
        </div>

        <div className="nav-links">
          <button 
            className={`nav-tab ${pageView === 'review' ? 'active' : ''}`}
            onClick={() => setPageView('review')}
          >
            <LayoutDashboard size={16} />
            Diagnostic Review
          </button>

          <button 
            className={`nav-tab ${pageView === 'inspector' ? 'active' : ''}`}
            onClick={() => setPageView('inspector')}
          >
            <Split size={16} />
            Split-Screen Inspector
          </button>

          <button 
            className={`nav-tab ${pageView === 'templates' ? 'active' : ''}`}
            onClick={() => setPageView('templates')}
          >
            <BookOpen size={16} />
            ATS Resume Templates
          </button>

          <button 
            className={`nav-tab ${pageView === 'history' ? 'active' : ''}`}
            onClick={() => setPageView('history')}
          >
            <Clock size={16} />
            My Account History ({history.length})
          </button>
        </div>

        <div className="auth-nav-actions">
          <div className="user-profile-menu">
            <div className="profile-pill">
              <span className="profile-avatar">{currentUser.full_name ? currentUser.full_name[0].toUpperCase() : 'U'}</span>
              <div className="user-meta-text">
                <span className="profile-name">{currentUser.full_name}</span>
                <span className="profile-email">{currentUser.email}</span>
              </div>
            </div>
            <button className="signout-btn" onClick={handleSignOut} title="Sign Out of Your Account">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </nav>

      <main className="workspace-full">
        {/* VIEW 1: DIAGNOSTIC REVIEW */}
        {pageView === 'review' && (
          <>
            {/* STATE A: Show Input & Upload Box Always */}
            <section className="input-section-container">
              <div className="input-grid">
                <div className="input-card">
                  <div className="card-heading">
                    <div>
                      <p className="section-kicker">Step 1</p>
                      <h2>Upload PDF Resume</h2>
                    </div>
                    <span className="secure-note">Private Account File</span>
                  </div>
                  <UploadBox file={file} setFile={setFile} />
                </div>

                <div className="input-card">
                  <div className="card-heading">
                    <div>
                      <p className="section-kicker">Step 2</p>
                      <h2>Target Job Requirements</h2>
                    </div>
                    <span className={hasJobDescription ? 'optional-tag is-ready' : 'optional-tag'}>
                      {hasJobDescription ? 'Ready' : 'Recommended'}
                    </span>
                  </div>
                  <textarea
                    value={jobDescription}
                    onChange={(event) => setJobDescription(preserveJobDescriptionLayout(event.target.value))}
                    placeholder="Paste job description requirements or target job title (e.g. Data Analyst)…"
                    aria-label="Target job description"
                  />
                  <div className="job-card-footer">
                    <span>{jobDescription.length.toLocaleString()} characters</span>
                    <span>Tip: Type job title or paste requirements.</span>
                  </div>
                </div>
              </div>

              {error && <div className="error-message" role="alert">{error}</div>}

              <div className="button-group-row">
                <button className="analyze-button" onClick={handleAnalyze} disabled={loading}>
                  {loading ? <Loader2 className="animate-spin" size={19} /> : <Sparkles size={19} />}
                  {loading ? 'Analyzing with Intelligent Engine…' : 'Run ATS Diagnostic Scan'}
                  {!loading && <ArrowRight size={19} />}
                </button>
              </div>
            </section>
            
            {!results && <EmptyInsights name={currentUser.full_name} />}

            {/* STATE B: SCAN REPORT ACTIVE -> Clean Full-Width Diagnostic Review (No Upload Cards!) */}
            {results && (
              <div className="dashboard-results-container clean-report-mode">
                
                {/* 1-Click PDF Generator Banner */}
                <div className="pdf-quick-banner">
                  <div className="banner-info">
                    <Download size={24} className="banner-icon" />
                    <div>
                      <h3>1-Click Corrected ATS PDF Generator</h3>
                      <p>Automatically inserts missing hard skills, fixes 2-column layout bleeding, and guarantees 0 Mirror Parser warnings.</p>
                    </div>
                  </div>
                  <button className="download-ats-pdf-btn-large" onClick={() => handleGlobalDownloadPDF(results)} disabled={downloadingPDF}>
                    {downloadingPDF ? <Loader2 className="animate-spin" size={18} /> : <Download size={18} />}
                    {downloadingPDF ? "Generating Corrected PDF..." : "Download Corrected ATS PDF"}
                  </button>
                </div>

                <div className="analysis-layout">
                  {/* Left Column: Score Gauge & Metrics */}
                  <aside className="insights-column">
                    <ATSGauge results={results} />

                    {results.word_metrics && (
                      <div className="metrics-card">
                        <h3><FileText size={16} /> Resume Health Metrics</h3>
                        <div className="metrics-grid">
                          <div className="metric-item">
                            <span>Word Count</span>
                            <strong>{results.word_metrics.total_words} words</strong>
                          </div>
                          <div className="metric-item">
                            <span>Action Verbs</span>
                            <strong>{results.word_metrics.action_verb_count} detected</strong>
                          </div>
                        </div>
                        <p className="metrics-note">{results.word_metrics.feedback}</p>
                      </div>
                    )}
                  </aside>

                  {/* Right Column: Tabbed Detailed Analysis */}
                  <section className="results-main-column">
                    <div className="dashboard-tabs">
                      <button 
                        className={`tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
                        onClick={() => setActiveTab('skills')}
                      >
                        <Target size={16} /> Skill Alignment
                      </button>
                      <button 
                        className={`tab-btn ${activeTab === 'actions' ? 'active' : ''}`}
                        onClick={() => setActiveTab('actions')}
                      >
                        <Lightbulb size={16} /> Action Plan & Bullets
                      </button>
                      <button 
                        className={`tab-btn ${activeTab === 'structure' ? 'active' : ''}`}
                        onClick={() => setActiveTab('structure')}
                      >
                        <CheckCircle2 size={16} /> Format Advisory
                      </button>
                      <button 
                        className={`tab-btn ${activeTab === 'mirror' ? 'active' : ''}`}
                        onClick={() => setActiveTab('mirror')}
                      >
                        <Eye size={16} /> Mirror Parser Text
                      </button>
                    </div>

                    <div className="tab-content-area">
                      {activeTab === 'skills' && (
                        <KeywordPanel 
                          skillsBreakdown={results.skills_breakdown} 
                          matched={results.matched_keywords} 
                          missing={results.missing_keywords} 
                        />
                      )}

                      {activeTab === 'actions' && (
                        <Suggestions 
                          suggestions={results.suggestions} 
                          bulletRecommendations={results.bullet_recommendations}
                        />
                      )}

                      {activeTab === 'structure' && (
                        <ResumeChanges changes={results.resume_changes} />
                      )}

                      {activeTab === 'mirror' && (
                        <MirrorParserView 
                          rawText={results.raw_extracted_text}
                          layoutAlerts={results.layout_alerts}
                          hasMultiColumnRisk={results.has_multi_column_risk}
                        />
                      )}
                    </div>
                  </section>
                </div>
              </div>
            )}
          </>
        )}

        {/* VIEW 2: SPLIT-SCREEN RESUME INSPECTOR */}
        {pageView === 'inspector' && (
          <ResumeInspector 
            rawText={results ? results.raw_extracted_text : ""}
            skillsBreakdown={results ? results.skills_breakdown : {}}
            suggestions={results ? results.suggestions : []}
            bulletRecommendations={results ? results.bullet_recommendations : []}
          />
        )}

        {/* VIEW 3: RESUME TEMPLATES */}
        {pageView === 'templates' && <ResumeTemplates />}

        {/* VIEW 4: HISTORY & SAVED DIAGNOSTIC REVIEWS */}
        {pageView === 'history' && (
          <div className="history-view-container">
            <div className="history-header">
              <div>
                <h2>Saved Scan Reports & Diagnostic Reviews</h2>
                <p className="history-subhead">Stored securely under your account ({currentUser.email}). Click any report to view its full Diagnostic Review.</p>
              </div>
              <button onClick={clearHistory} className="clear-history-btn">
                <Trash2 size={15} /> Clear History View
              </button>
            </div>
            {history.length > 0 ? (
              <div className="history-full-list">
                {history.map((item) => (
                  <div key={item.id} className="history-report-card">
                    <div className="report-card-left">
                      <div className={`history-score-ring ${item.score >= 80 ? 'good' : item.score >= 50 ? 'medium' : 'low'}`}>
                        <strong>{item.score}</strong>
                        <span>/100</span>
                      </div>
                      <div className="report-meta-info">
                        <div className="report-title-row">
                          <h3>Target Role: {formatDisplayRole(item.jobDomain)}</h3>
                          <span className="scan-date-tag"><Clock size={12} /> {item.date}</span>
                        </div>
                        <p className="report-filename"><FileText size={13} /> {item.resumeFilename || "Uploaded_Resume.pdf"}</p>
                        
                        {item.results && item.results.matched_keywords && (
                          <div className="history-tags-preview">
                            <span className="history-tag match">✓ {item.results.matched_keywords.length} Matched Skills</span>
                            <span className="history-tag missing">! {item.results.missing_keywords ? item.results.missing_keywords.length : 0} Missing Skills</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="report-card-actions">
                      <button 
                        className="open-review-btn" 
                        onClick={() => handleSelectHistoryScanInCurrentTab(item)}
                        title="View this diagnostic review report"
                      >
                        <Eye size={15} /> View Full Diagnostic Review
                      </button>
                      
                      <button 
                        className="delete-report-btn" 
                        onClick={() => handleDeleteScan(item.id)}
                        title="Delete this scan report from your account"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-history-text">No saved scan reports found for your account. Run a scan to auto-save your first report!</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

function EmptyInsights({ name }) {
  return (
    <div className="empty-insights">
      <div className="empty-score">
        <LayoutDashboard size={32} />
      </div>
      <h2>Welcome, {name}! Your Workspace is Ready</h2>
      <p>Upload your PDF resume and target job description to run fuzzy matching, inspect raw machine-extracted text, and auto-save scans to your account.</p>
    </div>
  );
}

export default App;