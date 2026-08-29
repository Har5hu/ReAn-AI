import React from 'react';
import { FileCheck2, Target, Layout, FileText } from 'lucide-react';

function scoreTone(score) { 
  return score >= 80 ? 'good' : score >= 50 ? 'medium' : 'low'; 
}

function ATSGauge({ results }) {
  const score = Math.round(results?.overall_score || 0);
  const subScores = results?.sub_scores || {};
  
  const pillars = [
    { label: 'Keyword Coverage', score: subScores.keyword_coverage || results?.keyword_score || 0, weight: '45%', icon: Target, color: '#6366f1' },
    { label: 'Format Readability', score: subScores.format_readability || results?.section_score || 0, weight: '30%', icon: Layout, color: '#10b981' },
    { label: 'Word Count & Density', score: subScores.word_count_density || results?.impact_score || 0, weight: '25%', icon: FileText, color: '#f59e0b' },
  ];

  return (
    <section className="score-card">
      <div className="score-card-title">
        <div className="score-icon">
          <FileCheck2 size={20} />
        </div>
        <div>
          <p className="eyebrow">Diagnostic Score</p>
          <h2>ATS Compatibility</h2>
        </div>
      </div>

      <div className={`score-ring ${scoreTone(score)}`} style={{ '--score': `${score * 3.6}deg` }}>
        <div>
          <strong>{score}</strong>
          <span>/100</span>
        </div>
      </div>

      <p className="score-summary">
        {score >= 80 
          ? 'Strong ATS alignment! Ready for corporate submission with high recruiter match.' 
          : score >= 60 
          ? 'Good foundation. Implement key recommendations below to boost ranking.' 
          : 'Action required. Formatting or key technical skills need immediate optimization.'}
      </p>

      <div className="dimension-list">
        {pillars.map(({ label, score: pScore, weight, icon: Icon, color }) => (
          <div className="dimension" key={label}>
            <div className="dimension-header">
              <span className="dimension-title">
                <Icon size={14} style={{ color }} /> {label} <small>({weight})</small>
              </span>
              <strong>{Math.round(pScore)}%</strong>
            </div>
            <div className="progress-bar-bg">
              <div 
                className="progress-bar-fill" 
                style={{ width: `${Math.max(0, Math.min(100, pScore))}%`, background: color }} 
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ATSGauge;
