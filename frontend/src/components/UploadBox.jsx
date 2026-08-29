import { useCallback, useState } from 'react';
import { CheckCircle2, FileText, Upload, X } from 'lucide-react';

function UploadBox({ file, setFile }) {
  const [isDragging, setIsDragging] = useState(false);
  const acceptFile = useCallback((candidate) => {
    if (candidate) setFile(candidate);
  }, [setFile]);
  const handleDrag = useCallback((event) => {
    event.preventDefault();
    setIsDragging(event.type !== 'dragleave');
  }, []);
  const handleDrop = useCallback((event) => {
    event.preventDefault();
    setIsDragging(false);
    acceptFile(event.dataTransfer.files?.[0]);
  }, [acceptFile]);

  if (file) return (
    <div className="upload-box upload-complete">
      <div className="uploaded-icon"><FileText size={28} /></div>
      <div className="uploaded-copy"><div className="uploaded-title"><strong>{file.name}</strong><CheckCircle2 size={18} /></div><span>{(file.size / 1024 / 1024).toFixed(1)} MB · Ready to review</span></div>
      <button className="remove-file" onClick={() => setFile(null)} aria-label="Remove resume"><X size={18} /></button>
    </div>
  );

  return (
    <div className={`upload-box ${isDragging ? 'is-dragging' : ''}`} onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}>
      <input id="resume-upload" type="file" accept=".pdf,.doc,.docx" onChange={(event) => acceptFile(event.target.files?.[0])} />
      <div className="upload-icon"><Upload size={24} /></div>
      <h3>Drop your resume here</h3>
      <p>or choose a file from your computer</p>
      <label htmlFor="resume-upload" className="browse-button">Choose file</label>
      <small>Supports PDF, DOC and DOCX up to 10MB</small>
    </div>
  );
}

export default UploadBox;
