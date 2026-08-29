import React, { useState } from 'react';
import { Eye, AlertTriangle, CheckCircle, Copy, FileText } from 'lucide-react';

function MirrorParserView({ rawText = "", layoutAlerts = [], hasMultiColumnRisk = false }) {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="mirror-parser-card">
      <div className="card-heading">
        <div>
          <div className="kicker-tag">
            <Eye size={15} /> Mirror Parser (ATS Machine View)
          </div>
          <h2>Raw Extracted Text</h2>
          <p>See exactly how a corporate ATS reads your document line-by-line before keyword scanning.</p>
        </div>
        <button className="toggle-mirror-btn" onClick={() => setIsOpen(!isOpen)}>
          <FileText size={16} />
          {isOpen ? "Hide Raw Text" : "View Raw ATS Text"}
        </button>
      </div>

      {hasMultiColumnRisk && (
        <div className="layout-warning-banner">
          <AlertTriangle size={20} className="warning-icon" />
          <div>
            <strong>Formatting Warning: Multi-Column Layout Detected</strong>
            <p>Standard corporate ATS parsers process PDFs line-by-line across the page, which mashing multi-column layouts together. Switch to a single-column layout for 100% readability.</p>
          </div>
        </div>
      )}

      {layoutAlerts.length > 0 && !hasMultiColumnRisk && (
        <div className="layout-info-banner">
          <CheckCircle size={18} />
          <span>{layoutAlerts[0]}</span>
        </div>
      )}

      {isOpen && (
        <div className="raw-text-container">
          <div className="raw-text-toolbar">
            <span className="raw-text-badge">Parsed with pdfplumber (Max 2 Pages)</span>
            <button className="copy-btn" onClick={handleCopy}>
              <Copy size={14} />
              {copied ? "Copied!" : "Copy Text"}
            </button>
          </div>
          <pre className="raw-text-block">{rawText || "No text extracted."}</pre>
        </div>
      )}
    </section>
  );
}

export default MirrorParserView;
