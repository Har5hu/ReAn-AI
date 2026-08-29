from intelligent_matcher import intelligent_skill_match, clean_skill_name

print("=== TESTING EXCEL & NORMALIZATION FIXES ===")

resume_sample = """
Manchili Sri Datha Kamala Harshini
Email: harshini@example.com | Phone: 9876543210
EXPERIENCE:
- Utilized MS Excel and Python to analyze customer churn datasets.
- Performed exploratory data analysis and predictive modeling.
- Demonstrated strong decision making and problem solving skills.
"""

jd_skills = ["excel", "exploratory datum analysis", "decision", "decision making", "problem solve", "pandas", "sql"]

res = intelligent_skill_match(resume_sample, jd_skills)

matched_h = [m["name"] for m in res["matched_hard"]]
matched_s = [m["name"] for m in res["matched_soft"]]
missing_h = res["missing_hard"]

print("Matched Hard:", matched_h)
print("Matched Soft:", matched_s)
print("Missing Hard:", missing_h)

# Assertions
assert "Excel" in matched_h, "FAILED: Excel should be in Matched Hard!"
assert "Exploratory Data Analysis" in matched_h, "FAILED: Exploratory Data Analysis should be matched!"
assert "Decision Making" in matched_s, "FAILED: Decision Making should be in Matched Soft!"
assert "Problem Solving" in matched_s, "FAILED: Problem Solving should be in Matched Soft!"
assert "Decision" not in missing_h and "Decision" not in matched_h, "FAILED: 'Decision' should not duplicate 'Decision Making'!"
assert "Exploratory Datum Analysis" not in missing_h, "FAILED: 'Datum' should be normalized to 'Data'!"

print("\n[PASS] ALL EXCEL AND NORMALIZATION TESTS PASSED 100%!")
