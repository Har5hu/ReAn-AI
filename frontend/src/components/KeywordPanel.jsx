import React from 'react';
import { Check, Plus, Sparkles, Award } from 'lucide-react';

function KeywordPanel({ skillsBreakdown = {}, matched = [], missing = [] }) {
  const matchedHard = skillsBreakdown.matched_hard || [];
  const matchedSoft = skillsBreakdown.matched_soft || [];
  const missingHard = skillsBreakdown.missing_hard || missing;
  const missingSoft = skillsBreakdown.missing_soft || [];
  const taxonomyBridges = skillsBreakdown.taxonomy_bridges || [];
  const fuzzyMatches = skillsBreakdown.fuzzy_matches || [];

  const totalSkillsCount = matchedHard.length + matchedSoft.length + missingHard.length + missingSoft.length;

  return (
    <section className="keyword-card">
      <div className="keyword-heading">
        <div>
          <p className="section-kicker">Role alignment</p>
          <h2>Skill & Taxonomy Breakdown</h2>
        </div>
        <span className="skill-count-badge">{totalSkillsCount} Evaluated</span>
      </div>

      {/* Taxonomy Bridges */}
      {taxonomyBridges.length > 0 && (
        <div className="taxonomy-bridge-section">
          <h3>
            <Sparkles size={16} className="taxonomy-icon" /> Smart Taxonomy Bridges
          </h3>
          <div className="bridge-list">
            {taxonomyBridges.map((bridge, idx) => (
              <div key={`bridge-${idx}`} className="bridge-badge">
                <Award size={14} />
                <span>{bridge.explanation}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Matched Hard Technical Skills */}
      {matchedHard.length > 0 && (
        <div className="skill-group">
          <h3>
            <Check size={15} className="text-green" /> Matched Hard Skills
          </h3>
          <div className="keyword-list">
            {matchedHard.map((word) => (
              <span className="keyword matched-hard" key={word}>
                {word}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Hard Technical Skills */}
      {missingHard.length > 0 && (
        <div className="skill-group">
          <h3>
            <Plus size={15} className="text-red" /> Missing Hard Skills (Priority)
          </h3>
          <div className="keyword-list">
            {missingHard.map((word) => (
              <span className="keyword missing-hard" key={word}>
                {word}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Soft Skills */}
      {(matchedSoft.length > 0 || missingSoft.length > 0) && (
        <div className="skill-group">
          <h3>
            <Sparkles size={15} className="text-amber" /> Soft Skills Evaluation
          </h3>
          <div className="keyword-list">
            {matchedSoft.map((word) => (
              <span className="keyword matched-soft" key={`soft-m-${word}`}>
                ✓ {word}
              </span>
            ))}
            {missingSoft.map((word) => (
              <span className="keyword missing-soft" key={`soft-miss-${word}`}>
                + {word}
              </span>
            ))}
          </div>
        </div>
      )}

      {totalSkillsCount === 0 && (
        <p className="no-keywords">Paste a job description to extract required hard & soft skills.</p>
      )}
    </section>
  );
}

export default KeywordPanel;
