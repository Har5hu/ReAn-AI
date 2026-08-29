import React, { useState } from 'react';
import { Lightbulb, ChevronRight, Copy, Check, Sparkles, CheckCircle2 } from 'lucide-react';

function Suggestions({ suggestions = [], bulletRecommendations = [] }) {
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopyBullet = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="recommendations-container">
      {/* Ready-to-Use Simple Experience Bullet Points */}
      {bulletRecommendations.length > 0 && (
        <section className="feedback-card bullet-recommendations-card">
          <div className="feedback-heading">
            <div className="feedback-icon accent-sparkle">
              <Sparkles size={19} />
            </div>
            <div>
              <p className="section-kicker">Simple Bullet Examples</p>
              <h2>Ready-to-Copy Experience Bullets</h2>
            </div>
          </div>
          <p className="card-subtext">
            Copy these natural, practical bullet points directly into your Work Experience or Projects section:
          </p>

          <div className="bullet-cards-list">
            {bulletRecommendations.map((item, idx) => (
              <div key={`bullet-rec-${idx}`} className="bullet-card-item">
                <div className="bullet-card-header">
                  <span className="kw-badge">Missing Tool: <strong>{item.keyword}</strong></span>
                  <button 
                    className="copy-bullet-btn" 
                    onClick={() => handleCopyBullet(item.example_bullet, idx)}
                  >
                    {copiedIndex === idx ? <Check size={14} /> : <Copy size={14} />}
                    {copiedIndex === idx ? "Copied!" : "Copy Bullet"}
                  </button>
                </div>
                <div className="bullet-example-text">"{item.example_bullet}"</div>
                <div className="bullet-tip-text">💡 {item.tip}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Step-by-Step Action Plan */}
      <section className="feedback-card">
        <div className="feedback-heading">
          <div className="feedback-icon">
            <Lightbulb size={19} />
          </div>
          <div>
            <p className="section-kicker">Step-by-Step Action Plan</p>
            <h2>Specific Resume Improvements</h2>
          </div>
        </div>

        {suggestions.length > 0 ? (
          <div className="feedback-list">
            {suggestions.map((suggestion, index) => (
              <div className="feedback-item" key={`suggestion-${index}`}>
                <span className="item-num">{String(index + 1).padStart(2, '0')}</span>
                <p>{suggestion}</p>
                <ChevronRight size={17} className="chevron" />
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-feedback">
            <CheckCircle2 size={20} className="text-green" />
            <p>Your resume formatting and content align great with standard ATS practices!</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default Suggestions;