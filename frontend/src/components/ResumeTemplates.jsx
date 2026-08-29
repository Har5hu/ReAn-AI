import React, { useState } from 'react';
import { Copy, Check, FileText, Download, Sparkles } from 'lucide-react';

const TEMPLATES = [
  {
    id: "data-analyst",
    title: "Data Analyst & Data Scientist ATS Template",
    category: "Technical / Analytics",
    description: "100% single-column layout optimized for Data Analysts, Business Intelligence, and Data Scientists.",
    content: `FIRST LAST NAME
City, State | Phone: (123) 456-7890 | Email: email@example.com | LinkedIn: linkedin.com/in/username

PROFESSIONAL SUMMARY
Data Analyst with X years of experience analyzing large-scale datasets, building interactive dashboards, and designing automated data pipelines. Skilled in SQL, Python, Tableau, and Machine Learning with a track record of optimizing reporting workflows by 30%.

TECHNICAL SKILLS
- Programming Languages: Python, SQL, R
- Analytics & Visualization: Tableau, Power BI, Excel, Matplotlib, Seaborn
- Data Processing & Databases: Pandas, NumPy, PostgreSQL, MySQL, Snowflake
- Methodologies: Data Analysis, Data Visualization, ETL, A/B Testing, Statistics

WORK EXPERIENCE
Data Analyst | Tech Solutions Inc. | City, State (2022 - Present)
- Spearheaded quarterly KPI reporting by engineering interactive Tableau dashboards, decreasing manual report prep time by 40%.
- Executed complex SQL queries and Pandas scripts across 50M+ records to uncover customer churn patterns, boosting retention by 15%.
- Partnered with cross-functional stakeholders to define business requirements and deliver automated daily ETL pipelines.

Data Analyst Intern | Innovation Corp | City, State (2021 - 2022)
- Analyzed sales transaction data using SQL and Excel to evaluate product performance across 5 regional markets.
- Built predictive forecasting models in Python achieving 91% accuracy for quarterly revenue estimation.

EDUCATION
State University, City, State
Bachelor of Technology in Computer Science & Engineering | CGPA: 3.8/4.0 | Graduated: May 2022

PROJECTS
Customer Segmentation ML Model (Python, Scikit-Learn, Pandas)
- Trained K-Means clustering model to segment 100K+ user profiles, identifying 4 high-value customer personas.`
  },
  {
    id: "software-engineer",
    title: "Software & Backend Engineer ATS Template",
    category: "Software Engineering",
    description: "Clean single-column layout focused on architecture, APIs, data structures, and microservices.",
    content: `FIRST LAST NAME
City, State | Phone: (123) 456-7890 | Email: email@example.com | GitHub: github.com/username

TECHNICAL SKILLS
- Languages: Java, Python, JavaScript, TypeScript, SQL
- Frameworks & Backend: Node.js, Express.js, Django, Spring Boot, REST APIs
- DevOps & Cloud: AWS, Docker, Kubernetes, CI/CD, Git, PostgreSQL, Redis
- Core Concepts: Data Structures, Object-Oriented Design, Microservices, System Design

WORK EXPERIENCE
Software Engineer | Enterprise Software Co. | City, State (2022 - Present)
- Developed and deployed high-throughput RESTful microservices in Node.js serving 200K+ daily active users.
- Optimized PostgreSQL database schema and query indexes, reducing API latency from 450ms to 110ms.
- Containerized application services using Docker and configured CI/CD pipelines for seamless deployment.

Backend Developer Intern | CloudTech Solutions | City, State (2021 - 2022)
- Implemented authentication and user permission services using JWT and Spring Boot.
- Created automated integration tests achieving 88% unit code coverage across core backend modules.

EDUCATION
State University, City, State
Bachelor of Science in Computer Science | CGPA: 3.9/4.0 | Graduated: May 2022

PROJECTS
Distributed Task Queue Service (Python, Redis, Docker)
- Designed an asynchronous worker task queue using Redis and Docker, processing up to 10K jobs per minute.`
  },
  {
    id: "entry-level",
    title: "Entry-Level / Student ATS Template",
    category: "University / Student",
    description: "Highlights Education, Academic Projects, and Technical Skills first for recent graduates.",
    content: `FIRST LAST NAME
City, State | Phone: (123) 456-7890 | Email: email@example.com | LinkedIn: linkedin.com/in/username

EDUCATION
State University, City, State
Bachelor of Technology in Computer Science & Engineering | CGPA: 8.8/10.0 | Graduated: May 2024
Relevant Coursework: Data Structures, Database Systems, Machine Learning, Data Visualization, Statistics

TECHNICAL SKILLS
- Programming: Python, SQL, C++, HTML/CSS
- Tools & Libraries: Pandas, NumPy, Tableau, Power BI, Git, Excel
- Core Competencies: Data Analysis, Problem Solving, Communication, Teamwork

ACADEMIC PROJECTS
E-Commerce Sales Insights Dashboard (Tableau, SQL, Python)
- Extracted and cleaned 20K+ transaction rows using Python and SQL.
- Designed an interactive Tableau dashboard showcasing monthly sales trends, profit margins, and regional growth.

Heart Disease Prediction Model (Python, Scikit-Learn)
- Built a Logistic Regression classification model to predict cardiac risk factors with 87% accuracy.

LEADERSHIP & EXTRA-CURRICULAR
Student Technical Club Lead | State University (2023 - 2024)
- Organized 3 coding workshops for 150+ students on Python data analysis fundamentals.`
  }
];

function ResumeTemplates() {
  const [copiedId, setCopiedId] = useState(null);

  const handleCopy = (content, id) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="templates-container">
      <div className="templates-header">
        <div>
          <p className="eyebrow"><Sparkles size={14} /> ATS Resume Gallery</p>
          <h2>100% ATS-Compliant Single-Column Templates</h2>
          <p>Copy these single-column markdown templates directly into Microsoft Word or Google Docs for 100% parser readability.</p>
        </div>
      </div>

      <div className="templates-grid">
        {TEMPLATES.map((tmpl) => (
          <div key={tmpl.id} className="template-card">
            <div className="template-card-header">
              <div>
                <span className="template-cat-tag">{tmpl.category}</span>
                <h3>{tmpl.title}</h3>
                <p>{tmpl.description}</p>
              </div>
              <button 
                className="copy-template-btn"
                onClick={() => handleCopy(tmpl.content, tmpl.id)}
              >
                {copiedId === tmpl.id ? <Check size={15} /> : <Copy size={15} />}
                {copiedId === tmpl.id ? "Copied Template!" : "Copy Template Text"}
              </button>
            </div>

            <div className="template-preview-box">
              <pre className="template-text">{tmpl.content}</pre>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResumeTemplates;
