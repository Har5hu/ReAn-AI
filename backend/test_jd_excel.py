from keyword_extractor import extract_keywords
from intelligent_matcher import intelligent_skill_match

sample_jd = """
Data Analyst Role Requirements:
Looking for a Data Analyst with experience in SQL, Python, Excel, Tableau, Data Visualization, and Data Analysis.
Must be able to build reports and handle data cleaning.
"""

sample_resume = """
Manchili Sri Datha Kamala Harshini
Skills: SQL, Python, Advanced Excel, Tableau, Data Analysis.
"""

extracted = extract_keywords(sample_jd)
print("Extracted Keywords from JD:", extracted)

match_res = intelligent_skill_match(sample_resume, extracted)
matched_h = [m["name"] for m in match_res["matched_hard"]]

print("Matched Hard Skills:", matched_h)

assert "excel" in extracted or "Excel" in [e.capitalize() for e in extracted], "FAILED: Excel missing from extracted JD keywords!"
assert "Excel" in matched_h, "FAILED: Excel missing from Matched Hard Skills!"

print("\n[PASS] EXCEL JD EXTRACTION & MATCHING TEST PASSED 100%!")
