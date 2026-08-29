import re

PROPER_CASE_MAP = {
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "aws": "AWS",
    "gcp": "GCP",
    "azure": "Azure",
    "api": "API",
    "apis": "APIs",
    "rest": "REST",
    "restful": "RESTful API",
    "json": "JSON",
    "ci/cd": "CI/CD",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "nlp": "NLP",
    "tableau": "Tableau",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "pandas": "Pandas",
    "panda": "Pandas",
    "numpy": "NumPy",
    "python": "Python",
    "r": "R",
    "excel": "Excel",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "advanced excel": "Excel",
    "msexcel": "Excel",
    "excel sheet": "Excel",
    "excel sheets": "Excel",
    "excel experience": "Excel",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "sqlite": "SQLite",
    "oracle": "Oracle",
    "sql server": "SQL Server",
    "mssql": "SQL Server",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "react": "React",
    "vue": "Vue.js",
    "angular": "Angular",
    "node.js": "Node.js",
    "express": "Express.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analysis",
    "data visualization": "Data Visualization",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "xgboost": "XGBoost",
    "etl": "ETL",
    "datum": "Data Analysis",
    "datum analysis": "Data Analysis",
    "data cleaning": "Data Cleaning",
    "datum cleaning": "Data Cleaning",
    "exploratory data analysis": "Exploratory Data Analysis",
    "exploratory datum analysis": "Exploratory Data Analysis",
    "eda": "Exploratory Data Analysis",
    "decision": "Decision Making",
    "decision making": "Decision Making",
    "data driven decision making": "Data-Driven Decision Making",
    "data-driven decision making": "Data-Driven Decision Making",
    "problem solve": "Problem Solving",
    "problem solving": "Problem Solving",
    "business understanding": "Business Understanding",
    "stakeholder management": "Stakeholder Management",
    "stakeholders": "Stakeholder Management",
    "stakeholder": "Stakeholder Management",
    "report": "Reporting",
    "reporting": "Reporting",
    "requirement": "Requirements",
    "requirements": "Requirements",
    "analyst": "Data Analysis",
    "analytics": "Data Analysis",
    "analytical": "Data Analysis",
    "b.tech": "B.Tech",
    "bsc": "B.Sc",
    "msc": "M.Sc",
    "m.tech": "M.Tech"
}

def clean_skill_name(term):
    if not term:
        return ""
    t_lower = term.lower().strip()
    if t_lower in PROPER_CASE_MAP:
        return PROPER_CASE_MAP[t_lower]
    # Replace 'datum' with 'data'
    t_lower = t_lower.replace("datum", "data")
    if t_lower in PROPER_CASE_MAP:
        return PROPER_CASE_MAP[t_lower]
    return " ".join(word.capitalize() for word in t_lower.split())

def normalize_root(term):
    """Normalize singular/plural forms to avoid duplicate terms."""
    t = term.lower().strip().replace("datum", "data")
    if t in ("decision", "decision making"):
        return "decision making"
    if t.endswith('s') and not t.endswith('ss') and len(t) > 3:
        t = t[:-1]
    return t

SKILL_TAXONOMY = {
    "data visualization": ["tableau", "power bi", "powerbi", "matplotlib", "seaborn", "looker", "d3.js", "plotly", "grafana", "qlik"],
    "machine learning": ["ml", "scikit-learn", "sklearn", "tensorflow", "pytorch", "xgboost", "lightgbm", "keras", "deep learning", "neural networks"],
    "data analysis": ["pandas", "numpy", "sql", "excel", "ms excel", "microsoft excel", "advanced excel", "data analytics", "statistics", "r", "analytics", "analyst", "analytical"],
    "cloud computing": ["aws", "azure", "gcp", "google cloud", "amazon web services", "cloud"],
    "databases": ["postgresql", "postgres", "mysql", "mongodb", "sqlite", "oracle", "sql server", "mssql", "snowflake", "redis", "dynamodb"],
    "devops": ["docker", "kubernetes", "k8s", "ci/cd", "jenkins", "terraform", "ansible", "git", "github", "gitlab"],
    "frontend": ["react", "vue", "angular", "html", "css", "javascript", "typescript", "tailwind", "bootstrap", "next.js"],
    "backend": ["node.js", "express", "django", "flask", "fastapi", "spring boot", "java", "python", "c#", ".net"],
    "data engineering": ["spark", "pyspark", "hadoop", "airflow", "kafka", "dbt", "etl", "data pipeline", "data pipelines"]
}

SYNONYMS = {
    "datum": "data",
    "datum analysis": "data analysis",
    "exploratory datum analysis": "exploratory data analysis",
    "datum cleaning": "data cleaning",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "advanced excel": "excel",
    "msexcel": "excel",
    "excel sheet": "excel",
    "excel experience": "excel",
    "panda": "pandas",
    "analyst": "data analysis",
    "analytics": "data analysis",
    "analytical": "data analysis",
    "decision": "decision making",
    "problem solve": "problem solving",
    "ml": "machine learning",
    "nlp": "natural language processing",
    "ai": "artificial intelligence",
    "k8s": "kubernetes",
    "postgres": "postgresql",
    "mssql": "sql server",
    "aws": "amazon web services",
    "gcp": "google cloud",
    "powerbi": "power bi",
    "scikit-learn": "sklearn",
    "js": "javascript",
    "ts": "typescript",
    "py": "python"
}

SOFT_SKILL_INDICATORS = {
    "communication": ["communication", "communicated", "present", "presented", "wrote", "stakeholder", "speak", "briefed", "client", "explained", "documented", "collaboration"],
    "leadership": ["leadership", "led", "managed", "spearheaded", "directed", "mentored", "supervised", "head", "lead", "guided", "oversaw", "managed a team"],
    "teamwork": ["teamwork", "team", "collaboration", "collaborated", "partnered", "cross-functional", "group", "coordinated", "team player"],
    "collaboration": ["collaboration", "collaborated", "partnered", "teamwork", "cross-functional", "coordinated"],
    "problem solving": ["problem solving", "problem solve", "resolved", "solved", "troubleshot", "optimized", "debugged", "fixed", "analyzed", "reduced", "improved", "solution"],
    "decision making": ["decision making", "decision", "decisions", "data driven decision making", "data-driven decision making", "strategy", "strategic"],
    "data driven decision making": ["data driven decision making", "data-driven decision making", "decision making", "data-driven"],
    "business understanding": ["business understanding", "business intelligence", "domain knowledge", "business strategy", "stakeholders"],
    "stakeholder management": ["stakeholder management", "stakeholders", "stakeholder", "client", "clients", "executives", "management"],
    "stakeholders": ["stakeholders", "stakeholder", "stakeholder management", "client", "clients", "executives", "management"],
    "report": ["report", "reporting", "dashboards", "dashboard", "metrics", "analytics"],
    "reporting": ["reporting", "report", "dashboards", "dashboard", "metrics", "analytics"]
}

STOP_WORDS = {
    "and", "the", "for", "with", "has", "was", "are", "from", "that", 
    "this", "these", "those", "have", "had", "not", "but", "also", 
    "into", "over", "under", "again", "then", "once", "here", "there",
    "requirement", "requirements", "description", "responsibilities",
    "end", "an", "or", "in", "at", "to", "of", "on"
}

def is_hard_skill(skill_name):
    s_clean = skill_name.lower().strip()
    if s_clean in SOFT_SKILL_INDICATORS:
        return False
    soft_terms = {"management", "communication", "leadership", "teamwork", "problem solving", "problem solve", "adaptability", "creativity", "decision making", "decision", "business understanding", "stakeholders", "stakeholder management", "report", "reporting"}
    return s_clean not in soft_terms

def intelligent_skill_match(resume_text, jd_keywords):
    resume_lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    
    body_lines = []
    for idx, line in enumerate(resume_lines):
        line_lower = line.lower()
        if idx < 3 and ("@" in line_lower or re.search(r"\b\d{10}\b", line) or re.search(r"phone|email|address|linkedin", line_lower)):
            continue
        body_lines.append(line)
        
    resume_body_text = "\n".join(body_lines) if body_lines else resume_text
    resume_lower = resume_body_text.lower()

    matched_hard = []
    matched_soft = []
    missing_hard = []
    missing_soft = []
    
    taxonomy_bridges = []
    fuzzy_matches = []
    
    consumed_roots = set()
    
    for raw_skill in jd_keywords:
        skill_clean_label = clean_skill_name(raw_skill)
        skill_key = raw_skill.lower().strip()
        skill_root = normalize_root(skill_key)
        
        if skill_root in consumed_roots or skill_key in STOP_WORDS or skill_clean_label.lower() in STOP_WORDS:
            continue
            
        hard_flag = is_hard_skill(skill_key)
        found = False
        match_type = "direct"
        match_detail = None
        
        # 1. Soft Skill Indicator Matching
        if not hard_flag:
            indicators = SOFT_SKILL_INDICATORS.get(skill_key, [skill_key])
            if any(re.search(rf"\b{re.escape(ind)}\b", resume_lower) for ind in indicators):
                found = True
                match_type = "contextual_soft"
                match_detail = f"Demonstrated in bullet points ({skill_clean_label})"
        
        # 2. Direct Exact, Synonym, or Substring Match (Special handling for Excel variants)
        if not found:
            skill_normalized = SYNONYMS.get(skill_key, skill_key)
            if skill_key in ("excel", "ms excel", "microsoft excel", "advanced excel") or skill_normalized == "excel":
                pattern = r"\b(excel|ms excel|microsoft excel|advanced excel|msexcel)\b"
                norm_pattern = pattern
            else:
                pattern = rf"\b{re.escape(skill_key)}s?\b"
                norm_pattern = rf"\b{re.escape(skill_normalized)}s?\b"
            
            if re.search(pattern, resume_lower) or re.search(norm_pattern, resume_lower):
                found = True
                match_type = "direct"
            
        # 3. Taxonomy Bridge Match
        if not found and hard_flag:
            if skill_key in SKILL_TAXONOMY:
                child_tools = SKILL_TAXONOMY[skill_key]
                found_children = [clean_skill_name(c) for c in child_tools if re.search(rf"\b{re.escape(c)}\b", resume_lower)]
                if found_children:
                    found = True
                    match_type = "taxonomy"
                    bridge_desc = f"Matched via Taxonomy: {', '.join(found_children[:2])} -> {skill_clean_label}"
                    match_detail = bridge_desc
                    taxonomy_bridges.append({
                        "jd_skill": skill_clean_label,
                        "found_tools": found_children,
                        "explanation": bridge_desc
                    })
            else:
                for parent_cat, children in SKILL_TAXONOMY.items():
                    if skill_key in children:
                        if re.search(rf"\b{re.escape(parent_cat)}\b", resume_lower):
                            found = True
                            match_type = "taxonomy"
                            parent_label = clean_skill_name(parent_cat)
                            bridge_desc = f"Matched via Taxonomy: {parent_label} -> {skill_clean_label}"
                            match_detail = bridge_desc
                            taxonomy_bridges.append({
                                "jd_skill": skill_clean_label,
                                "found_tools": [parent_label],
                                "explanation": bridge_desc
                            })
                            break

        consumed_roots.add(skill_root)
        consumed_roots.add(normalize_root(skill_clean_label))
        
        skill_payload = {
            "name": skill_clean_label,
            "match_type": match_type,
            "detail": match_detail
        }
        
        if found:
            if hard_flag:
                matched_hard.append(skill_payload)
            else:
                matched_soft.append(skill_payload)
        else:
            if hard_flag:
                missing_hard.append(skill_clean_label)
            else:
                missing_soft.append(skill_clean_label)

    return {
        "matched_hard": matched_hard,
        "matched_soft": matched_soft,
        "missing_hard": missing_hard,
        "missing_soft": missing_soft,
        "taxonomy_bridges": taxonomy_bridges,
        "fuzzy_matches": []
    }
