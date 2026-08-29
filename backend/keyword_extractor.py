import re
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.skill_extractor_class import SkillExtractor
from skillNer.general_params import SKILL_DB

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    try:
        nlp = spacy.load("en_core_web_lg")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")

print("Loading SkillNER AI Model... (This takes 2-3 seconds)")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
print("SUCCESS: AI Extraction Engine ready!")

JD_BLOCKLIST = {
    "job description", "requirements", "job requirements", "responsibilities", 
    "key responsibilities", "qualifications", "about the role", "role overview", 
    "summary", "job summary", "about us", "who you are", "what you will do",
    "ability", "experience", "work experience", "good", 
    "strong", "excellent", "fast", "support", "basic", "english", "working", 
    "candidate", "the candidate", "years", "year", "role", "team", "understanding", "knowledge",
    "reports", "statistic", "stakeholder"
}

GENERIC_NOISE_TERMS = {
    "skill", "skills", "requirement", "requirements", "qualification", "qualifications",
    "responsibility", "responsibilities", "ability", "abilities", "knowledge",
    "experience", "experiences", "task", "tasks", "duty", "duties", "role", "roles"
}

def clean_extracted_term(term):
    if not term or not isinstance(term, str):
        return ""
    t = term.lower().strip()
    t = re.sub(r'^(the|a|an)\s+', '', t)
    t = re.sub(r'[^a-z0-9\s\+\#\-\.]', '', t)
    return t.strip()

def normalize_skill_variant(term):
    t = clean_extracted_term(term)
    if not t:
        return ""
    if re.search(r'\b(ms excel|microsoft excel|advanced excel|excel skills)\b', t):
        return "Excel"
    if re.search(r'\b(ms word|microsoft word)\b', t):
        return "Word"
    if re.search(r'\b(ms powerpoint|microsoft powerpoint)\b', t):
        return "PowerPoint"
    if re.search(r'\b(power bi|powerbi)\b', t):
        return "Power BI"
    if re.search(r'\b(tableau)\b', t):
        return "Tableau"
    if re.search(r'\b(python|python3)\b', t):
        return "Python"
    if re.search(r'\b(sql|mysql|postgresql|sqlite)\b', t):
        return "SQL"
    return t.title()

def extract_job_keywords(job_description_text):
    if not job_description_text or not job_description_text.strip():
        return []

    text_clean = job_description_text.strip()
    keywords = set()

    # 1. Direct Regex Technical Keyword Matcher
    KNOWN_TECH_PATTERNS = [
        (r'\bsql\b', "SQL"), (r'\bpython\b', "Python"), (r'\bexcel\b', "Excel"),
        (r'\btableau\b', "Tableau"), (r'\bpower bi\b', "Power BI"), (r'\baws\b', "AWS"),
        (r'\bdocker\b', "Docker"), (r'\bkubernetes\b', "Kubernetes"), (r'\bpandas\b', "Pandas"),
        (r'\bnumpy\b', "NumPy"), (r'\breact\b', "React"), (r'\bnode\.?js\b', "Node.js"),
        (r'\bdata cleaning\b', "Data Cleaning"), (r'\bexploratory data analysis\b', "Exploratory Data Analysis"),
        (r'\bdata analysis\b', "Data Analysis"), (r'\bstatistics\b', "Statistics"),
        (r'\bdecision making\b', "Decision Making"), (r'\bproblem solving\b', "Problem Solving"),
        (r'\bcommunication\b', "Communication Skills"), (r'\bdashboards?\b', "Dashboards"),
        (r'\bdatasets?\b', "Datasets"), (r'\breporting\b', "Reporting"), (r'\bstakeholder\b', "Stakeholder Management"),
        (r'\bgis\b', "GIS"), (r'\bqgis\b', "QGIS"), (r'\barcgis\b', "ArcGIS"), (r'\bgeopandas\b', "GeoPandas"),
        (r'\bshapely\b', "Shapely"), (r'\brasterio\b', "Rasterio"), (r'\bfolium\b', "Folium"),
        (r'\bgeojson\b', "GeoJSON"), (r'\bkml\b', "KML"), (r'\bmachine learning\b', "Machine Learning"),
        (r'\bdeep learning\b', "Deep Learning"), (r'\bscikit-learn\b', "Scikit-learn"), (r'\bmatplotlib\b', "Matplotlib"),
        (r'\bseaborn\b', "Seaborn"), (r'\bregression\b', "Regression"), (r'\bclassification\b', "Classification"),
        (r'\bclustering\b', "Clustering"), (r'\bforecasting\b', "Forecasting"), (r'\banomaly detection\b', "Anomaly Detection"),
        (r'\bpredictive analysis\b', "Predictive Analysis"), (r'\bartificial intelligence\b', "Artificial Intelligence")
    ]
    for pattern, name in KNOWN_TECH_PATTERNS:
        if re.search(pattern, text_clean, re.IGNORECASE):
            keywords.add(name)

    # 2. SkillNER Extraction
    try:
        annotations = skill_extractor.annotate(text_clean)
        results = annotations.get("results", {})
        
        full_matches = results.get("full_matches", [])
        for match in full_matches:
            doc_node = match.get("doc_node", "")
            norm = normalize_skill_variant(doc_node)
            if norm and norm.lower() not in JD_BLOCKLIST and norm.lower() not in GENERIC_NOISE_TERMS:
                keywords.add(norm)
                
        ngram_matches = results.get("ngram_scored", [])
        for match in ngram_matches:
            doc_node = match.get("doc_node", "")
            norm = normalize_skill_variant(doc_node)
            if norm and len(norm) > 2 and norm.lower() not in JD_BLOCKLIST and norm.lower() not in GENERIC_NOISE_TERMS:
                keywords.add(norm)
    except Exception as e:
        print(f"SkillNER extraction notice: {e}")

    # Deduplicate normalized root terms
    deduped = {}
    for kw in keywords:
        norm_kw = normalize_skill_variant(kw)
        key = norm_kw.lower()
        if key not in deduped:
            deduped[key] = norm_kw

    return sorted(list(deduped.values()))

# Alias for app.py import compatibility
extract_keywords = extract_job_keywords