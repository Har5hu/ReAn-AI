import { AlertCircle, CheckCircle2, Highlighter } from 'lucide-react';

function ResumeChanges({ changes = [] }) {
  if (!changes.length) return null;

  return <section className="changes-card">
    <div className="changes-heading"><div className="changes-icon"><Highlighter size={19} /></div><div><p>Highlighted for your resume</p><h2>Changes to make</h2></div></div>
    <p className="changes-note">Only add details that genuinely describe your experience.</p>
    <div className="change-list">{changes.map((change, index) => <article className={`change-item ${change.type}`} key={`${change.title}-${index}`}><span>{change.type === 'keyword' || change.type === 'alignment' ? <AlertCircle size={17} /> : <CheckCircle2 size={17} />}</span><div><strong>{change.title}</strong><p>{change.detail}</p></div></article>)}</div>
  </section>;
}

export default ResumeChanges;
