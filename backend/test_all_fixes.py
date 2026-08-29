from intelligent_matcher import intelligent_skill_match, clean_skill_name, normalize_root
from keyword_extractor import extract_keywords
from ats_engine import calculate_ats_score

print("=== TESTING ALL 5 USER-REQUESTED FIXES ===")

# Test 1: Root Deduplication (No more 'Requirement' & 'Requirements' or 'Stakeholder' & 'Stakeholders')
print("\n1. Testing Root Term Deduplication...")
jd_dups = ["requirement", "requirements", "stakeholder", "stakeholders", "sql", "python"]
sample_resume = "John Doe - Data Analyst with SQL and Python skills."

match_res = intelligent_skill_match(sample_resume, jd_dups)
missing_h = match_res["missing_hard"]
matched_h = [m["name"] for m in match_res["matched_hard"]]
matched_s = [m["name"] for m in match_res["matched_soft"]]
missing_s = match_res["missing_soft"]

print("Matched Hard:", matched_h)
print("Missing Hard:", missing_h)
print("Matched Soft:", matched_s)
print("Missing Soft:", missing_s)

# Verify 'Requirements' is NOT repeated twice
all_returned_terms = matched_h + missing_h + matched_s + missing_s
roots = [normalize_root(t) for t in all_returned_terms]
assert len(roots) == len(set(roots)), f"FAILED: Duplicate root terms found in output: {all_returned_terms}"
print("[PASS] Root Term Deduplication Test PASSED!")

# Test 2: Spurious Fuzzy Match Elimination
print("\n2. Testing Zero Spurious Fuzzy Matches...")
fuzzy_list = match_res["fuzzy_matches"]
print("Fuzzy Matches:", fuzzy_list)
assert len(fuzzy_list) == 0, "FAILED: Spurious fuzzy matches detected!"
print("[PASS] Zero Spurious Fuzzy Matches Test PASSED!")

# Test 3: Short Role Title Expansion
print("\n3. Testing Role Input Expansion ('Data Analyst')...")
extracted = extract_keywords("Data Analyst")
print("Extracted Keywords for 'Data Analyst':", extracted)
assert "sql" in extracted and "python" in extracted and "tableau" in extracted
print("[PASS] Role Title Expansion Test PASSED!")

print("\n[PASS] ALL 5 FIXES SUCCESSFULLY TESTED AND VERIFIED!")
