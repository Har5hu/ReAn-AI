from resume_parser import extract_text_from_pdf
from intelligent_matcher import intelligent_skill_match, clean_skill_name
from ats_engine import calculate_ats_score

print("=== TESTING BACKEND PHASES ===")

# Test 1: Intelligent Matcher (Fuzzy & Taxonomy & Terminology Normalization)
jd_keywords = ["data visualization", "pandas", "datum", "python", "sql", "communication"]
sample_resume = """
John Doe - Data Analyst
Experience:
- Built interactive Tableau dashboards for marketing analytics.
- Analyzed large data sets using Pandas and SQL.
- Strong communication and leadership skills.
"""

print("\n1. Testing Intelligent Matcher...")
match_res = intelligent_skill_match(sample_resume, jd_keywords)
print("Matched Hard:", [m["name"] for m in match_res["matched_hard"]])
print("Matched Soft:", [m["name"] for m in match_res["matched_soft"]])
print("Missing Hard:", match_res["missing_hard"])
print("Taxonomy Bridges:", match_res["taxonomy_bridges"])

assert any(m["name"] in ["Data Analysis", "Data"] for m in match_res["matched_hard"]), "Datum term normalization failed"
assert len(match_res["taxonomy_bridges"]) > 0, "Taxonomy bridge failed"
print("[PASS] Intelligent Matcher & Terminology Normalization Test PASSED!")

# Test 2: ATS Engine Scoring & Soft Skill Evaluation
print("\n2. Testing ATS Engine Scoring...")
score_res = calculate_ats_score(sample_resume, jd_keywords, "We are seeking a Data Analyst skilled in Python, SQL, Tableau, and Pandas.")
print("Overall Score:", score_res["overall_score"])
print("Sub-scores:", score_res["sub_scores"])

assert "overall_score" in score_res
assert "sub_scores" in score_res
assert score_res["sub_scores"]["soft_skills_score"] >= 85, "Soft skills evaluation failed"
print("[PASS] ATS Engine Scoring & Soft Skill Test PASSED!")
