import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from intelligent_matcher import clean_skill_name

def clean_raw_lines(resume_text):
    """Strips out page marker noise ('--- PAGE 1 ---', 'PAGE 1') and normalizes whitespace."""
    raw_lines = resume_text.split('\n')
    cleaned = []
    for line in raw_lines:
        line_str = line.strip()
        if not line_str:
            continue
        if re.search(r"^---\s*PAGE\s*\d+\s*---$", line_str, re.IGNORECASE):
            continue
        if re.search(r"^PAGE\s*\d+$", line_str, re.IGNORECASE):
            continue
        cleaned.append(line_str)
    return cleaned

def parse_resume_into_sections(resume_text):
    lines = clean_raw_lines(resume_text)
    
    sections = {
        "header": [],
        "summary": [],
        "education": [],
        "skills": [],
        "experience": [],
        "projects": [],
        "certificates": []
    }
    
    current_sec = "header"
    
    sec_patterns = [
        ("summary", [r"^summary$", r"^profile summary$", r"^professional summary$", r"^profile$", r"^about me$"]),
        ("education", [r"^education$", r"^academic background$", r"^qualifications$"]),
        ("skills", [r"^technical skills$", r"^skills$", r"^skills & tools$", r"^technologies$"]),
        ("experience", [r"^work experience$", r"^experience$", r"^internship$", r"^internships$", r"^employment history$"]),
        ("projects", [r"^projects$", r"^project$", r"^academic projects$", r"^key projects$"]),
        ("certificates", [r"^certifications$", r"^certificates$", r"^courses$", r"^certifications & awards$"])
    ]
    
    for line in lines:
        line_lower = line.lower()
        matched_sec = None
        
        for sec_name, patterns in sec_patterns:
            if any(re.search(p, line_lower) for p in patterns):
                matched_sec = sec_name
                break
                
        if matched_sec:
            current_sec = matched_sec
        else:
            sections[current_sec].append(line)
            
    return sections

def is_bullet_line(line):
    line_str = line.strip()
    if not line_str: return False
    first_char = line_str[0]
    return not first_char.isalnum()

def strip_bullet_prefix(line):
    line_str = line.strip()
    if not line_str: return ""
    return re.sub(r"^[^a-zA-Z0-9]+", "", line_str).strip()

def extract_candidate_header(header_lines):
    if not header_lines:
        return "APPLICANT RESUME", "Email: email@example.com | Location: City, State"
        
    name = header_lines[0].strip()
    if "@" in name or len(name) > 60:
        name = "APPLICANT RESUME"
        contact_items = header_lines
    else:
        contact_items = header_lines[1:]
        
    contacts = []
    for line in contact_items:
        cleaned = line.replace('\uf0b2', '').replace('\uf0e0', '').replace('\uf095', '').replace('\uf08c', '').strip()
        if cleaned:
            contacts.append(cleaned)
            
    contact_str = " | ".join(contacts) if contacts else ""
    contact_str = re.sub(r'\s+\|\s+', ' | ', contact_str)
    return name, contact_str

def build_single_column_ats_pdf(resume_text, missing_keywords=None):
    """
    Builds a 100% single-column ATS-compliant PDF resume with clean executive typography.
    - Standard Helvetica & Helvetica-Bold fonts.
    - Bullet text is rendered in NORMAL (non-bold) font matching standard resume formatting.
    - Zero multi-column bleeding (100% linear flow).
    - Auto-inserts missing hard keywords seamlessly.
    """
    if missing_keywords is None:
        missing_keywords = []
        
    sections = parse_resume_into_sections(resume_text)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    name_style = ParagraphStyle(
        'ExecutiveName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ExecutiveContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        alignment=1,
        spaceAfter=14
    )
    
    section_heading_style = ParagraphStyle(
        'ExecutiveSectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=2,
        textTransform='uppercase'
    )
    
    body_style = ParagraphStyle(
        'ExecutiveBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )

    item_title_style = ParagraphStyle(
        'ExecutiveItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=6,
        spaceAfter=2
    )

    bullet_style = ParagraphStyle(
        'ExecutiveBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=3
    )

    story = []

    header_lines = sections.get("header", [])
    name, contact_info = extract_candidate_header(header_lines)
    
    story.append(Paragraph(name, name_style))
    if contact_info:
        story.append(Paragraph(contact_info, contact_style))
    else:
        story.append(Spacer(1, 8))

    summary_lines = sections.get("summary", [])
    if summary_lines:
        story.append(Paragraph("PROFILE SUMMARY", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        summary_text = " ".join([line.strip() for line in summary_lines if line.strip()])
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 4))

    edu_lines = sections.get("education", [])
    if edu_lines:
        story.append(Paragraph("EDUCATION", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for line in edu_lines:
            clean_line = strip_bullet_prefix(line)
            if "college" in line.lower() or "school" in line.lower() or "university" in line.lower() or "institute" in line.lower():
                story.append(Paragraph(f"<b>{clean_line}</b>", item_title_style))
            else:
                story.append(Paragraph(clean_line, body_style))
        story.append(Spacer(1, 4))

    skills_lines = sections.get("skills", [])
    story.append(Paragraph("SKILLS", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
    
    existing_skills_text = "\n".join(skills_lines) if skills_lines else ""
    cleaned_missing = [clean_skill_name(kw) for kw in missing_keywords if kw.lower() not in existing_skills_text.lower()]
    
    if skills_lines:
        merged_missing = False
        for s_line in skills_lines:
            clean_s = strip_bullet_prefix(s_line)
            
            if cleaned_missing and not merged_missing and "soft skill" not in clean_s.lower():
                clean_s += ", " + ", ".join(cleaned_missing)
                merged_missing = True
                
            story.append(Paragraph(f"&bull; {clean_s}", bullet_style))
            
        if cleaned_missing and not merged_missing:
            story.append(Paragraph(f"&bull; Core Competencies: {', '.join(cleaned_missing)}", bullet_style))
    else:
        default_skills = ["Python", "SQL", "R", "Excel", "Tableau", "Power BI"] + cleaned_missing
        story.append(Paragraph(f"&bull; Programming Languages & Tools: {', '.join(default_skills)}", bullet_style))

    story.append(Spacer(1, 4))

    exp_lines = sections.get("experience", [])
    if exp_lines:
        story.append(Paragraph("EXPERIENCE & INTERNSHIPS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        merged_exp = []
        for line in exp_lines:
            if is_bullet_line(line) or "pvt" in line.lower() or "ltd" in line.lower() or "internship" in line.lower() or "company" in line.lower():
                merged_exp.append(line.strip())
            else:
                if merged_exp:
                    merged_exp[-1] += " " + line.strip()
                else:
                    merged_exp.append(line.strip())
                    
        for line in merged_exp:
            if is_bullet_line(line):
                clean_bullet = strip_bullet_prefix(line)
                story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))
            else:
                story.append(Paragraph(f"<b>{line}</b>", item_title_style))
        story.append(Spacer(1, 4))

    proj_lines = sections.get("projects", [])
    if proj_lines:
        story.append(Paragraph("PROJECTS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        merged_proj = []
        for line in proj_lines:
            if is_bullet_line(line):
                merged_proj.append(line.strip())
            else:
                if merged_proj:
                    merged_proj[-1] += " " + line.strip()
                else:
                    merged_proj.append(line.strip())
                    
        for line in merged_proj:
            clean_bullet = strip_bullet_prefix(line)
            if ":" in clean_bullet:
                parts = clean_bullet.split(":", 1)
                formatted_bullet = f"<b>{parts[0]}:</b>{parts[1]}"
                story.append(Paragraph(f"&bull; {formatted_bullet}", bullet_style))
            else:
                story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))
        story.append(Spacer(1, 4))

    cert_lines = sections.get("certificates", [])
    if cert_lines:
        story.append(Paragraph("CERTIFICATIONS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for line in cert_lines:
            clean_bullet = strip_bullet_prefix(line)
            story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
