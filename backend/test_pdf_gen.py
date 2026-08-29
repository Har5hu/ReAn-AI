from pdf_generator import build_single_column_ats_pdf
from resume_parser import extract_text_from_pdf
from ats_engine import calculate_ats_score

print("=== TESTING 1-CLICK OPTIMIZED ATS PDF GENERATOR ===")

sample_resume = """
John Doe
City, State | Phone: (123) 456-7890 | Email: john@example.com

PROFESSIONAL SUMMARY
Data Analyst with 2 years of experience analyzing datasets and building reports.

TECHNICAL SKILLS
SQL, Python, Excel, Tableau

WORK EXPERIENCE
Data Analyst | Tech Corp (2022 - Present)
- Built SQL queries and Tableau dashboards to track quarterly KPIs.

EDUCATION
State University, City, State
Bachelor of Technology in Computer Science | CGPA: 3.8/4.0
"""

missing_kw = ["pandas", "statistics", "exploratory data analysis"]

# 1. Build Single-Column ATS PDF
pdf_buf = build_single_column_ats_pdf(sample_resume, missing_kw)
pdf_bytes = pdf_buf.getvalue()

assert len(pdf_bytes) > 0, "FAILED: PDF buffer is empty!"
print(f"Generated PDF Size: {len(pdf_bytes)} bytes")

# 2. Parse generated PDF back with pdfplumber (Mirror Parser)
parsed = extract_text_from_pdf(pdf_buf)
extracted_text = parsed.get("raw_text", "")
layout_alerts = parsed.get("layout_alerts", [])
has_risk = parsed.get("has_multi_column_risk", False)

print("\n--- MIRROR PARSER VERIFICATION ---")
print("Raw Extracted Text Snippet:\n", extracted_text[:300])
print("Layout Alerts:", layout_alerts)
print("Has Multi-Column Risk:", has_risk)

# 3. Assertions
assert not has_risk, "FAILED: Generated PDF triggered multi-column risk!"
assert len(layout_alerts) == 0, "FAILED: Generated PDF triggered layout alerts!"
assert "Pandas" in extracted_text or "pandas" in extracted_text.lower(), "FAILED: Missing keyword 'Pandas' not inserted!"
assert "Statistics" in extracted_text or "statistics" in extracted_text.lower(), "FAILED: Missing keyword 'Statistics' not inserted!"

print("\n[PASS] PDF GENERATOR & MIRROR PARSER VERIFICATION PASSED 100%!")
