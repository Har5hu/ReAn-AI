from keyword_extractor import extract_keywords
from intelligent_matcher import intelligent_skill_match
from ats_engine import calculate_ats_score

print("=== TESTING EXACT VIDEO RECORDING SCENARIO ===")

# Resume text matching candidate resume from video
resume_text = """
MANCHILI SRI DATHA KAMALA HARSHINI
Email: harshini@example.com | Phone: 9876543210
EDUCATION
Bachelor of Technology in Computer Science - CGPA: 8.5/10

EXPERIENCE
Data Analyst Intern - Tech Corp
- Built interactive Tableau and Power BI dashboards for executive reporting.
- Executed SQL queries and Pandas data structures for data cleaning and ETL pipelines.
- Applied machine learning models for customer churn prediction.

SKILLS
Python, SQL, Tableau, Power BI, Excel, Pandas, Machine Learning, Communication, Data Visualization
"""

# Short role title entered by user in video
job_input = "Data Analyst"

print("\n1. Testing Keyword Extractor for short input 'Data Analyst'...")
keywords = extract_keywords(job_input)
print("Extracted Keywords for 'Data Analyst':", keywords)

print("\n2. Testing Intelligent Matcher on Candidate Resume...")
match_res = intelligent_skill_match(resume_text, keywords)
print("Matched Hard:", [m["name"] for m in match_res["matched_hard"]])
print("Matched Soft:", [m["name"] for m in match_res["matched_soft"]])
print("Missing Hard:", match_res["missing_hard"])
print("Fuzzy Matches:", match_res["fuzzy_matches"])

# Verify candidate name 'DATHA' is NOT in fuzzy matches
assert not any(f["resume_term"].lower() == "datha" for f in match_res["fuzzy_matches"]), "FAILED: 'DATHA' fuzzy matched!"
# Verify 'and' is NOT in fuzzy matches
assert not any(f["resume_term"].lower() == "and" for f in match_res["fuzzy_matches"]), "FAILED: 'and' fuzzy matched!"

print("\n3. Testing ATS Score Calculation...")
score_res = calculate_ats_score(resume_text, keywords, job_input)
print("Overall ATS Score:", score_res["overall_score"])
print("Sub-scores:", score_res["sub_scores"])

assert score_res["overall_score"] >= 80, f"Expected high score for well-matched resume, got {score_res['overall_score']}"
print("\n✅ VIDEO RECORDING SCENARIO FIXES TESTED AND PASSED!")
