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
    """Accurately detects all bullet variations including -, •, *, –, —, ◦, ▪, ▫, ➢, >"""
    line_str = line.strip()
    return bool(re.match(r"^[-•\*–—◦▪▫➢>]\s*", line_str))

def strip_bullet_prefix(line):
    line_str = line.strip()
    return re.sub(r"^[-•\*–—◦▪▫➢>]\s*", "", line_str).strip()

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
        if "@" in line or re.search(r"\d{10}", line) or re.search(r"linkedin|github|phone|email", line.lower()) or len(line) < 50:
            contacts.append(line)
            
    contact_str = "  |  ".join(contacts) if contacts else ""
    return name, contact_str

def build_single_column_ats_pdf(resume_text, missing_keywords=None):
    """
    Builds a 100% single-column ATS-compliant PDF resume with clean executive typography.
    - Standard Helvetica & Helvetica-Bold fonts.
    - Bullet text is rendered in NORMAL (non-bold) font matching standard resume formatting.
    - Zero multi-column bleeding (100% linear flow).
    - Auto-inserts missing hard keywords into Technical Skills.
    """
    if missing_keywords is None:
        missing_keywords = []
        
    sections = parse_resume_into_sections(resume_text)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Universal Clean Resume Typography
    name_style = ParagraphStyle(
        'ExecutiveName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ExecutiveContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )
    
    section_heading_style = ParagraphStyle(
        'ExecutiveSectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
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
        spaceBefore=4,
        spaceAfter=2
    )

    # Bullet points MUST use Helvetica (normal weight, NOT bold!)
    bullet_style = ParagraphStyle(
        'ExecutiveBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    story = []

    # 1. CANDIDATE HEADER
    header_lines = sections.get("header", [])
    name, contact_info = extract_candidate_header(header_lines)
    
    story.append(Paragraph(name, name_style))
    if contact_info:
        story.append(Paragraph(contact_info, contact_style))
    else:
        story.append(Spacer(1, 4))

    # 2. PROFILE SUMMARY
    summary_lines = sections.get("summary", [])
    if summary_lines:
        story.append(Paragraph("PROFILE SUMMARY", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        story.append(Paragraph(" ".join(summary_lines), body_style))
        story.append(Spacer(1, 4))

    # 3. EDUCATION
    edu_lines = sections.get("education", [])
    if edu_lines:
        story.append(Paragraph("EDUCATION", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for idx in range(0, len(edu_lines), 2):
            inst = edu_lines[idx]
            detail = edu_lines[idx+1] if idx+1 < len(edu_lines) else ""
            story.append(Paragraph(f"<b>{inst}</b>", item_title_style))
            if detail:
                story.append(Paragraph(detail, body_style))
        story.append(Spacer(1, 4))

    # 4. TECHNICAL SKILLS (With missing hard skills auto-inserted)
    skills_lines = sections.get("skills", [])
    story.append(Paragraph("SKILLS", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
    
    existing_skills_text = "\n".join(skills_lines) if skills_lines else ""
    cleaned_missing = [clean_skill_name(kw) for kw in missing_keywords if kw.lower() not in existing_skills_text.lower()]
    
    if skills_lines:
        for s_line in skills_lines:
            clean_s = strip_bullet_prefix(s_line)
            story.append(Paragraph(f"&bull; {clean_s}", bullet_style))
    else:
        story.append(Paragraph("&bull; Programming Languages & Tools: Python, SQL, R, Excel, Tableau, Power BI", bullet_style))

    if cleaned_missing:
        added_str = ", ".join(cleaned_missing)
        story.append(Paragraph(f"&bull; Additional Technical Skills (ATS Optimized): {added_str}", bullet_style))
        
    story.append(Spacer(1, 4))

    # 5. WORK EXPERIENCE / INTERNSHIP
    exp_lines = sections.get("experience", [])
    if exp_lines:
        story.append(Paragraph("EXPERIENCE & INTERNSHIPS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for line in exp_lines:
            if is_bullet_line(line):
                clean_bullet = strip_bullet_prefix(line)
                story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))
            else:
                story.append(Paragraph(f"<b>{line}</b>", item_title_style))
        story.append(Spacer(1, 4))

    # 6. PROJECTS
    proj_lines = sections.get("projects", [])
    if proj_lines:
        story.append(Paragraph("PROJECTS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for line in proj_lines:
            if is_bullet_line(line):
                clean_bullet = strip_bullet_prefix(line)
                story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))
            else:
                story.append(Paragraph(f"<b>{line}</b>", item_title_style))
        story.append(Spacer(1, 4))

    # 7. CERTIFICATIONS
    cert_lines = sections.get("certificates", [])
    if cert_lines:
        story.append(Paragraph("CERTIFICATIONS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#1e293b'), spaceBefore=1, spaceAfter=6))
        
        for line in cert_lines:
            if is_bullet_line(line):
                clean_bullet = strip_bullet_prefix(line)
                story.append(Paragraph(f"&bull; {clean_bullet}", bullet_style))
            else:
                story.append(Paragraph(f"&bull; {line}", bullet_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
