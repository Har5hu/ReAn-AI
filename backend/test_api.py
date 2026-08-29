import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

print("Generating valid test PDF resume...")
buffer = io.BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
c.drawString(100, 750, "HARSHINI - DATA SCIENTIST")
c.drawString(100, 730, "Email: harshini@example.com | Phone: (123) 456-7890")
c.drawString(100, 700, "EXPERIENCE")
c.drawString(100, 680, "Data Analyst - Tech Corp (2022 - Present)")
c.drawString(100, 660, "- Designed interactive Tableau dashboards to track quarterly sales KPIs.")
c.drawString(100, 640, "- Analyzed large datasets using Pandas and SQL to optimize query execution speed.")
c.drawString(100, 620, "- Built machine learning models for customer churn prediction.")
c.drawString(100, 590, "EDUCATION")
c.drawString(100, 570, "Bachelor of Technology in Computer Science - CGPA: 3.8/4.0")
c.drawString(100, 540, "SKILLS")
c.drawString(100, 520, "Python, SQL, Tableau, Pandas, Machine Learning, Communication")
c.save()

pdf_bytes = buffer.getvalue()

print("Sending PDF to http://127.0.0.1:5000/analyze ...")
url = "http://127.0.0.1:5000/analyze"
files = {'resume': ('harshini_resume.pdf', pdf_bytes, 'application/pdf')}
data = {'job_description': 'Seeking a Data Scientist skilled in Python, SQL, Tableau, Pandas, Machine Learning, and Datum analysis.'}

res = requests.post(url, files=files, data=data)
print("Status Code:", res.status_code)
json_data = res.json()

if res.status_code == 200:
    print("\n=== API DIAGNOSTIC RESPONSE ===")
    print("Overall Score:", json_data.get("overall_score"))
    print("Sub-scores:", json_data.get("sub_scores"))
    print("Skills Breakdown:", json_data.get("skills_breakdown"))
    print("Bullet Recommendations Count:", len(json_data.get("bullet_recommendations", [])))
    print("Raw Extracted Text Snippet:", json_data.get("raw_extracted_text", "")[:120] + "...")
    print("\n✅ API END-TO-END TEST SUCCESSFUL!")
else:
    print("API Error Response:", json_data)
