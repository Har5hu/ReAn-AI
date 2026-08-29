import re
from intelligent_matcher import intelligent_skill_match, is_hard_skill, clean_skill_name

# Simple, natural, non-jargon bullet templates tailored by keyword
NATURAL_BULLET_LIBRARY = {
    "sql": "Wrote SQL queries with aggregations and JOINs to extract customer transaction data from relational databases.",
    "python": "Developed Python scripts to automate daily data processing workflows and clean incoming datasets.",
    "tableau": "Built interactive Tableau dashboards to visualize monthly sales trends and executive KPI metrics.",
    "power bi": "Designed Power BI reports connecting multi-source datasets to monitor business performance.",
    "aws": "Deployed and managed cloud application files and databases on AWS using S3 and EC2 instances.",
    "docker": "Containerized application services using Docker to ensure consistent testing and deployment environments.",
    "machine learning": "Trained a Random Forest classification model in Python to predict customer churn with 88% accuracy.",
    "pandas": "Cleaned and transformed 100K+ raw dataset rows using Pandas and Python, removing duplicate records.",
    "numpy": "Used NumPy for numerical computations and array operations across multi-dimensional datasets.",
    "react": "Built responsive web interface components in React with state management and dynamic UI updates.",
    "node.js": "Created REST API endpoints using Node.js and Express to deliver backend data services.",
    "data cleaning": "Cleaned raw customer datasets by filtering null values, normalizing formats, and removing duplicate entries.",
    "exploratory data analysis": "Performed exploratory data analysis (EDA) using Python to identify key purchasing trends and sales patterns.",
    "data analysis": "Analyzed 50K+ sales records using SQL and Python to extract actionable business insights.",
    "statistics": "Applied statistical methods like mean, standard deviation, and A/B testing to measure campaign performance.",
    "reporting": "Automated weekly reporting workflows, reducing manual report preparation time from 4 hours to 20 minutes.",
    "stakeholder management": "Presented weekly data insights to team leads and stakeholders to guide project decisions.",
    "decision making": "Analyzed historical sales metrics to support strategic decision making for inventory allocation.",
    "problem solving": "Diagnosed and resolved data pipeline errors, restoring data accuracy across daily reports.",
    "communication": "Communicated complex technical findings clearly in written summaries and team presentations."
}

FALLBACK_PATTERNS = [
    "Used {kw} to analyze dataset records and support team project goals.",
    "Built a project workflow incorporating {kw} to process data efficiently.",
    "Applied {kw} to solve data formatting issues and improve report accuracy.",
    "Created custom scripts utilizing {kw} to organize and present project metrics."
]

SPECIFIC_ROLE_PATTERNS = [
    r"\b(data analyst)\b",
    r"\b(senior data analyst)\b",
    r"\b(junior data analyst)\b",
    r"\b(data scientist)\b",
    r"\b(data science undergraduate)\b",
    r"\b(data science intern)\b",
    r"\b(data engineer)\b",
    r"\b(software engineer)\b",
    r"\b(software developer)\b",
    r"\b(full stack developer)\b",
    r"\b(frontend developer)\b",
    r"\b(backend developer)\b",
    r"\b(cloud engineer)\b",
    r"\b(cloud intern)\b",
    r"\b(azure cloud intern)\b",
    r"\b(azure developer)\b",
    r"\b(aws engineer)\b",
    r"\b(business analyst)\b",
    r"\b(data science intern)\b",
    r"\b(data scientist)\b",
    r"\b(machine learning engineer)\b",
    r"\b(ai/ds engineer)\b",
    r"\b(ai engineer)\b",
    r"\b(python developer)\b",
    r"\b(web developer)\b"
]

def extract_specific_job_role(job_description, resume_text):
    """Extracts candidate's specific target job title (e.g. Data Analyst, Cloud Intern)."""
    text_to_search = (job_description + "\n" + resume_text).lower()
    
    for pattern in SPECIFIC_ROLE_PATTERNS:
        match = re.search(pattern, text_to_search, re.IGNORECASE)
        if match:
            return match.group(1).title()
            
    jd_lines = [l.strip() for l in job_description.split('\n') if l.strip()]
    if jd_lines and len(jd_lines[0]) < 45 and not any(kw in jd_lines[0].lower() for kw in ['requirement', 'responsibilit', 'qualification', 'about']):
        return jd_lines[0].title()
        
    return "Data Analyst / Data Scientist"

def generate_contextual_bullets(missing_keywords):
    """Generates simple, practical, non-jargon bullet point recommendations."""
    bullet_recommendations = []
    for idx, kw in enumerate(missing_keywords[:4]):
        kw_clean = clean_skill_name(kw)
        kw_lower = kw.lower()
        
        if kw_lower in NATURAL_BULLET_LIBRARY:
            example = NATURAL_BULLET_LIBRARY[kw_lower]
        else:
            pattern = FALLBACK_PATTERNS[idx % len(FALLBACK_PATTERNS)]
            example = pattern.format(kw=kw_clean)
            
        bullet_recommendations.append({
            "keyword": kw_clean,
            "example_bullet": example,
            "tip": f"Add this bullet under your Work Experience or Projects section where you used {kw_clean}."
        })
    return bullet_recommendations

def calculate_ats_score(resume_text, job_description_keywords, job_description="", layout_data=None):
    if layout_data is None:
        layout_data = {"layout_alerts": [], "has_multi_column_risk": False}
        
    resume_lower = resume_text.lower()
    specific_role = extract_specific_job_role(job_description, resume_text)
    
    # 1. Match Keywords
    matcher_res = intelligent_skill_match(resume_text, job_description_keywords)
    matched_hard = matcher_res["matched_hard"]
    matched_soft = matcher_res["matched_soft"]
    missing_hard = matcher_res["missing_hard"]
    missing_soft = matcher_res["missing_soft"]
    taxonomy_bridges = matcher_res.get("taxonomy_bridges", [])
    fuzzy_matches = matcher_res.get("fuzzy_matches", [])

    total_keywords = len(job_description_keywords) if job_description_keywords else 1
    total_matched = len(matched_hard) + len(matched_soft)
    keyword_score = round((total_matched / total_keywords) * 100) if total_keywords > 0 else 75
    keyword_score = max(0, min(100, keyword_score))

    # Hard vs Soft sub-scores
    hard_total = len(matched_hard) + len(missing_hard)
    soft_total = len(matched_soft) + len(missing_soft)
    hard_skill_score = round((len(matched_hard) / hard_total) * 100) if hard_total > 0 else 80
    soft_skill_score = round((len(matched_soft) / soft_total) * 100) if soft_total > 0 else 70

    # 2. Section Readability Scoring
    expected_sections = ["summary", "skills", "experience", "education", "projects"]
    found_sections = 0
    sections_missing = []
    
    for sec in expected_sections:
        if re.search(r"\b" + sec + r"\b", resume_lower):
            found_sections += 1
        else:
            sections_missing.append(sec.title())
            
    readability_score = round((found_sections / len(expected_sections)) * 100)
    
    if layout_data.get("has_multi_column_risk"):
        readability_score = max(40, readability_score - 20)

    # 3. Word Count & Action Verb Density
    words = resume_text.split()
    total_word_count = len(words)
    
    if total_word_count < 250:
        word_count_density_score = 60
        word_count_feedback = "Resume is concise (under 250 words). Add detail to experience bullets."
    elif 250 <= total_word_count <= 800:
        word_count_density_score = 95
        word_count_feedback = "Optimal word count for ATS parsing (250–800 words)."
    else:
        word_count_density_score = 75
        word_count_feedback = "Resume is lengthy (over 800 words). Trim verbose descriptions."

    action_verbs = ["developed", "built", "managed", "created", "designed", "implemented", "analyzed", "led", "spearheaded", "engineered", "gained", "executed", "trained", "cleaned", "automated", "performed"]
    action_verb_count = sum(1 for verb in action_verbs if verb in resume_lower)
    
    if action_verb_count >= 5:
        word_count_density_score = min(100, word_count_density_score + 5)

    has_numbers = bool(re.search(r"\b\d+%\b|\b\d+\+\b|\b\$\d+\b", resume_text))
    has_percentage = "%" in resume_text

    # 4. Overall Weighted Score: 45% Keywords, 30% Format, 25% Impact
    overall_score = round(
        (keyword_score * 0.45) +
        (readability_score * 0.30) +
        (word_count_density_score * 0.25)
    )
    overall_score = max(10, min(100, overall_score))

    # Suggestions & Action Plan
    suggestions = []
    resume_changes = []

    if missing_hard:
        missing_str = ", ".join(missing_hard[:3])
        suggestions.append(f"Insert missing technical skills ({missing_str}) directly into your TECHNICAL SKILLS line.")
        resume_changes.append({
            "title": "Insert Technical Skills",
            "detail": f"Add missing keywords '{missing_str}' to your skills section.",
            "type": "skill"
        })

    if not has_numbers:
        suggestions.append("Add 2-3 specific numbers or metrics (e.g., 'analyzed 50K+ rows', 'reduced prep time by 20%').")
        resume_changes.append({
            "title": "Add Quantitative Metrics",
            "detail": "Include percentages or volume metrics in experience bullets to highlight business impact.",
            "type": "impact"
        })

    if sections_missing:
        missing_sec_str = ", ".join(sections_missing)
        suggestions.append(f"Add standard section headers: {missing_sec_str}.")
        resume_changes.append({
            "title": "Add Missing Header",
            "detail": f"Include standard section heading '{missing_sec_str}'.",
            "type": "format"
        })

    bullet_recommendations = generate_contextual_bullets(missing_hard)

    return {
        "overall_score": overall_score,
        "job_domain": specific_role,
        "sub_scores": {
            "keyword_coverage": keyword_score,
            "format_readability": readability_score,
            "word_count_density": word_count_density_score,
            "hard_skills_score": hard_skill_score,
            "soft_skills_score": soft_skill_score
        },
        "skills_breakdown": {
            "matched_hard": [item["name"] for item in matched_hard],
            "matched_soft": [item["name"] for item in matched_soft],
            "missing_hard": missing_hard,
            "missing_soft": missing_soft,
            "taxonomy_bridges": taxonomy_bridges,
            "fuzzy_matches": fuzzy_matches
        },
        "matched_keywords": [item["name"] for item in matched_hard] + [item["name"] for item in matched_soft],
        "missing_keywords": missing_hard + missing_soft,
        "word_metrics": {
            "total_words": total_word_count,
            "action_verb_count": action_verb_count,
            "has_metrics": has_numbers or has_percentage,
            "feedback": word_count_feedback
        },
        "bullet_recommendations": bullet_recommendations,
        "suggestions": suggestions,
        "resume_changes": resume_changes,
        "layout_alerts": layout_data.get("layout_alerts", []),
        "has_multi_column_risk": layout_data.get("has_multi_column_risk", False)
    }