from intelligent_matcher import intelligent_skill_match, clean_skill_name
from keyword_extractor import extract_keywords

print("=== TESTING CLEAN MATCHING ENGINE & ZERO FUZZY NOISE ===")

# Test Case 1: Candidate Name & Synonym Matching
candidate_resume = """
Datha Kumar - Data Scientist
Email: datha@example.com | Phone: 9876543210
EXPERIENCE:
- Performed data cleaning and machine learning model training.
- Built SQL queries and Pandas data structures.
"""
jd_skills = ["dataset", "pandas", "cleaning", "machine learning", "sql", "datum"]

res = intelligent_skill_match(candidate_resume, jd_skills)
matched_names = [m["name"] for m in res["matched_hard"]]

print("Matched Hard:", matched_names)
print("Fuzzy Matches (Should be empty):", res["fuzzy_matches"])

# Verify fuzzy_matches is empty (no ugly fuzzy badges!)
assert len(res["fuzzy_matches"]) == 0, "FAILED: Raw fuzzy matches found!"
assert "Pandas" in matched_names, "PASSED: Pandas matched cleanly"
assert "SQL" in matched_names, "PASSED: SQL matched cleanly"
assert "Data Analysis" in matched_names, "PASSED: Datum mapped to Data Analysis cleanly"

print("[PASS] Clean Matching & Zero Fuzzy Noise Test PASSED!")
