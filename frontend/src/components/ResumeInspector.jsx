import React, { useState } from 'react';
import { Eye, Copy, Plus, CheckCircle, Lightbulb, FileText, AlertCircle } from 'lucide-react';

function ResumeInspector({ rawText = "", skillsBreakdown = {}, suggestions = [], bulletRecommendations = [] }) {
  const [copiedSection, setCopiedSection] = useState(null);

  const missingHard = skillsBreakdown.missing_hard || [];
  const matchedHard = skillsBreakdown.matched_hard || [];

  const handleCopyText = (text, name) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(name);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  // Generate a ready-to-copy Skills Section Block
  const formattedSkillsBlock = missingHard.length > 0 
    ? `Technical Skills: ${matchedHard.concat(missingHard).join(', ')}`
    : `Technical Skills: ${matchedHard.join(', ')}`;

  return (
    <div className="resume-inspector-container">
      <div className="inspector-grid">
        {/* Left Side: Uploaded Resume Viewer */}
        <div className="inspector-left-card">
          <div className="card-header">
            <div className="header-title">
              <FileText size={18} className="icon-purple" />
              <div>
                <h2>Your Resume Text</h2>
                <p>Exact document text extracted by the ATS machine parser.</p>
              </div>
            </div>
            <button 
              className="copy-btn-outline"
              onClick={() => handleCopyText(rawText, 'raw')}
            >
              <Copy size={14} />
              {copiedSection === 'raw' ? 'Copied Full Text!' : 'Copy Full Text'}
            </button>
          </div>

          <div className="resume-preview-box">
            <pre className="resume-text-view">{rawText || "No resume text parsed yet. Upload a PDF resume above."}</pre>
          </div>
        </div>

        {/* Right Side: Direct Inline Recommendations & Placement Guide */}
        <div className="inspector-right-card">
          <div className="card-header">
            <div className="header-title">
              <Lightbulb size={18} className="icon-amber" />
              <div>
                <h2>Where to Make Changes</h2>
                <p>Actionable line-by-line recommendations mapped to your resume sections.</p>
              </div>
            </div>
          </div>

          <div className="section-actions-list">
            {/* 1. Technical Skills Section Change */}
            <div className="action-card-item highlight-purple">
              <div className="action-card-header">
                <span className="section-tag">Target: Skills Section</span>
                {missingHard.length > 0 && (
                  <button 
                    className="copy-action-btn"
                    onClick={() => handleCopyText(formattedSkillsBlock, 'skills')}
                  >
                    <Copy size={13} />
                    {copiedSection === 'skills' ? 'Copied Skills Block!' : 'Copy Optimized Skills Line'}
                  </button>
                )}
              </div>
              <h3>Add Missing Technical Keywords</h3>
              <p>Add these missing keywords into your technical skills summary block:</p>
              <div className="keyword-chips-row">
                {missingHard.map((kw, i) => (
                  <span key={i} className="chip-missing">+ {kw}</span>
                ))}
                {missingHard.length === 0 && <span className="chip-matched">✓ All required technical hard skills present!</span>}
              </div>
              {missingHard.length > 0 && (
                <div className="suggested-line-box">
                  <strong>Ready-to-Paste Skills Line:</strong>
                  <code>"{formattedSkillsBlock}"</code>
                </div>
              )}
            </div>

            {/* 2. Education Section Formatting Advisory (2-Row Single-Column Format) */}
            <div className="action-card-item highlight-green">
              <div className="action-card-header">
                <span className="section-tag tag-green">Target: Education Section</span>
              </div>
              <h3>ATS-Safe Education Formatting (Single-Column)</h3>
              <p>To avoid ATS multi-column text mashing, format your education in 2 distinct rows rather than side-by-side columns:</p>
              <div className="education-format-example">
                <div className="edu-row"><strong>Row 1:</strong> Institution Name, City, State</div>
                <div className="edu-row"><strong>Row 2:</strong> Degree Name - CGPA: X.X/4.0 | Graduation Year</div>
              </div>
            </div>

            {/* 3. Work Experience Bullet Points Placement */}
            {bulletRecommendations.length > 0 && (
              <div className="action-card-item highlight-indigo">
                <div className="action-card-header">
                  <span className="section-tag tag-indigo">Target: Experience Bullet Points</span>
                </div>
                <h3>Incorporate Keywords into Experience Bullets</h3>
                <p>Add context-rich bullet points instead of keyword stuffing:</p>
                <div className="inspector-bullet-list">
                  {bulletRecommendations.slice(0, 3).map((item, idx) => (
                    <div key={idx} className="inspector-bullet-item">
                      <div className="bullet-kw-header">
                        <span>Keyword: <strong>{item.keyword}</strong></span>
                        <button 
                          className="copy-bullet-small"
                          onClick={() => handleCopyText(item.example_bullet, `bullet-${idx}`)}
                        >
                          <Copy size={12} /> {copiedSection === `bullet-${idx}` ? 'Copied!' : 'Copy'}
                        </button>
                      </div>
                      <p className="bullet-example">"{item.example_bullet}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResumeInspector;
