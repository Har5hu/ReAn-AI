import io
import re
import pdfplumber
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_source):
    """
    Extract raw text and layout diagnostic metadata from PDF using pdfplumber.
    Restricted to first 2 pages for performance and latency safety.
    Includes PyPDF2 fallback.
    """
    raw_text = ""
    pages_processed = 0
    layout_alerts = []
    has_multi_column_risk = False
    
    # Ensure stream is at start
    if hasattr(file_source, 'seek'):
        file_source.seek(0)
        
    try:
        with pdfplumber.open(file_source) as pdf:
            total_pages = len(pdf.pages)
            if total_pages > 2:
                layout_alerts.append(f"Resume has {total_pages} pages. ATS recommendation is 1-2 pages maximum. Only first 2 pages analyzed.")
            
            # Process maximum of first 2 pages for speed
            for page_num, page in enumerate(pdf.pages[:2], start=1):
                pages_processed += 1
                page_text = page.extract_text(layout=False) or ""
                raw_text += f"--- PAGE {page_num} ---\n" + page_text + "\n\n"
                
                # Check for multi-column text positioning risk
                words = page.extract_words()
                if words:
                    # Check x-coordinate distribution of text blocks
                    x0_coords = [w['x0'] for w in words]
                    page_width = page.width or 612
                    midpoint = page_width / 2
                    
                    left_column_words = sum(1 for x in x0_coords if x < midpoint - 20)
                    right_column_words = sum(1 for x in x0_coords if x > midpoint + 20)
                    
                    if left_column_words > 40 and right_column_words > 40:
                        has_multi_column_risk = True
                        
    except Exception as pdfplumber_err:
        print(f"pdfplumber failed: {pdfplumber_err}, attempting PyPDF2 fallback...")
        try:
            if hasattr(file_source, 'seek'):
                file_source.seek(0)
            reader = PdfReader(file_source)
            total_pages = len(reader.pages)
            for page_num, page in enumerate(reader.pages[:2], start=1):
                pages_processed += 1
                page_text = page.extract_text() or ""
                raw_text += f"--- PAGE {page_num} ---\n" + page_text + "\n\n"
        except Exception as pypdf2_err:
            print(f"PyPDF2 fallback also failed: {pypdf2_err}")
            
    if has_multi_column_risk:
        layout_alerts.append("Multi-column layout detected! Standard corporate ATS parsers may interleave text across columns (mashing Experience into Skills). Consider switching to a single-column layout.")

    return {
        "raw_text": raw_text.strip(),
        "pages_processed": pages_processed,
        "layout_alerts": layout_alerts,
        "has_multi_column_risk": has_multi_column_risk
    }