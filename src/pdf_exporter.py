import textwrap
from fpdf import FPDF

def generate_pdf_bytes(report_text, variant_id, gene, classification):
    """Converts the LLM report into an executive clinical PDF with header banners and clean sections."""
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Dark Slate Header Banner (Venice Vibe)
    pdf.set_fill_color(11, 15, 25) # Deep Obsidian
    pdf.rect(0, 0, 210, 36, 'F')
    
    pdf.set_text_color(16, 185, 129) # Emerald Green Accent
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, "COREVARIANT | Clinical Interpretation Dossier", ln=True)
    
    pdf.set_text_color(226, 232, 240) # Slate Light
    pdf.set_font("Helvetica", size=9.5)
    pdf.set_xy(10, 18)
    pdf.cell(0, 8, f"Variant: {variant_id}  |  Gene Locus: {gene}  |  ACMG Status: {classification}", ln=True)
    
    # Reset Text Colors for Body
    pdf.set_text_color(30, 41, 59)
    pdf.set_y(42)
    
    # 2. Body Text Engine
    for line in report_text.split('\n'):
        clean_line = line.replace('**', '').replace('•', '-').replace('\t', '    ')
        clean_line = clean_line.encode('latin-1', 'ignore').decode('latin-1').strip()
        
        if clean_line.startswith('---') or clean_line.startswith('==='):
            pdf.ln(2)
            continue
            
        if not clean_line:
            pdf.ln(3)
            continue
            
        # Section Headers (##)
        if line.startswith('##'):
            header_title = clean_line.replace('## ', '')
            pdf.ln(4)
            pdf.set_fill_color(241, 245, 249) # Subtle Gray Highlight Box
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 7, f"  {header_title}", ln=True, fill=True)
            pdf.set_text_color(30, 41, 59)
            pdf.ln(2)
        else:
            # Body Text Wrapped cleanly
            wrapped_lines = textwrap.wrap(clean_line, width=92)
            for chunk in wrapped_lines:
                pdf.set_font("Helvetica", size=9.5)
                pdf.cell(0, 5, chunk, ln=True)
                
    return bytes(pdf.output())
