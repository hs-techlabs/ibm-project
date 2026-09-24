import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_docx_requirements(output_path):
    doc = Document()
    
    # Page setup
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(40, 40, 40)
    
    # Title Block
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title.add_run("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)\n& PROJECT REQUIREMENTS DOCUMENT")
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub.add_run("Vanguard: Retail Revenue & Customer Decision Intelligence Platform\nIBM Project Submission Track: Data Analytics & Applied AI")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(79, 70, 229)
    r_sub.bold = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # Metadata Table
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Project Name", "Vanguard: Retail Decision Intelligence Platform"),
        ("Track / Domain", "IBM Applied Data Analytics & Business Intelligence"),
        ("Repository URL", "https://github.com/hs-techlabs/ibm-project.git"),
        ("Author / Organization", "Himanshu Sharma (HS TechLabs)"),
        ("Submission Status", "Final Deliverable Release — Ready for Evaluation")
    ]
    for i, (k, v) in enumerate(meta):
        c1, c2 = table.rows[i].cells
        c1.text = k
        c2.text = v
        set_cell_background(c1, "F1F5F9")
        set_cell_background(c2, "FFFFFF")
        c1.paragraphs[0].runs[0].font.bold = True
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        c2.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.width = Inches(2.2)
        c2.width = Inches(4.8)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # 1. Executive Summary
    h1 = doc.add_heading("1. Executive Summary & Purpose", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    p = doc.add_paragraph(
        "This document defines the Software Requirements Specification (SRS) for Vanguard, "
        "an enterprise-grade Decision Intelligence Platform built upon 533,878 real-world transactions "
        "from the UCI Machine Learning Repository. Vanguard bridges raw transaction databases and executive "
        "boardroom governance by operationalizing the continuum: Data → Information → Insights → Decisions → Actions. "
        "This specification articulates all functional capabilities, non-functional constraints, technical stack "
        "dependencies, and execution prerequisites required for formal IBM project evaluation."
    )
    p.paragraph_format.line_spacing = 1.15
    
    # 2. Scope & Problem Statement
    h1 = doc.add_heading("2. Problem Statement & Scope", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    p = doc.add_paragraph(
        "Multi-channel retail enterprises face escalating operational friction across cross-border freight, customer "
        "churn, return processing, and catalog inventory imbalances. Commercial leadership frequently operates with "
        "fragmented reporting lacking driver attribution and scenario simulation. Vanguard provides a unified, "
        "single-file executable architecture that answers six critical business questions: true net revenue after refunds, "
        "departmental margin velocity, RFM customer retention, international export arbitrage, SKU return risk, and "
        "pricing elasticity forecasting."
    )
    p.paragraph_format.line_spacing = 1.15
    
    # 3. Functional Requirements
    h1 = doc.add_heading("3. Functional Requirements (FR)", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    
    fr_items = [
        ("FR-01: Data Ingestion & Sanitization", 
         "The system MUST ingest 533k+ transactions, filter non-retail administrative codes (POST, BANK CHARGES, etc.), "
         "isolate returns (InvoiceNo starting with 'C' or negative Quantity), reconcile guest accounts, and provide high-speed caching."),
        ("FR-02: Executive Decision Cockpit", 
         "The system MUST display 6 core C-suite KPIs (Net Revenue, Gross Profit, Total Orders, AOV, Gross Margin %, and Return Rate %) "
         "with dynamic period-over-period delta badges and automated alert banners."),
        ("FR-03: Revenue & Sales Velocity Module", 
         "The system MUST render dual-axis monthly revenue versus order volume trends and an intraday weekday-by-hour order density heatmap."),
        ("FR-04: Catalog & Category Intelligence", 
         "The system MUST implement an automated 8-category department keyword taxonomy and compute cumulative Pareto 80/20 SKU curves."),
        ("FR-05: Algorithmic RFM Customer Segmentation", 
         "The system MUST compute Recency (days), Frequency (order count), and Monetary (total spend) quintiles (1-5), classifying "
         "customers into Champions, Loyalists, Promising New, At-Risk, and Hibernating cohorts with exportable CSVs."),
        ("FR-06: Corporate Risk & Opportunity Engine", 
         "The system MUST quantify domestic geographic over-reliance (UK concentration) and size cross-border wholesale expansion opportunities."),
        ("FR-07: Predictive Demand & Price Elasticity Simulator", 
         "The system MUST execute Holt-Winters time-series forecasting with 95% confidence intervals and dynamic interactive sliders "
         "for price change (-20% to +30%) and COGS inflation (-10% to +20%)."),
        ("FR-08: Consolidated Single-File Delivery", 
         "The entire dashboard MUST run from a consolidated, standalone project.py script without external database setup.")
    ]
    
    for code, desc in fr_items:
        p = doc.add_paragraph()
        run_code = p.add_run(code + ": ")
        run_code.bold = True
        run_code.font.color.rgb = RGBColor(79, 70, 229)
        p.add_run(desc)
        p.paragraph_format.space_after = Pt(4)
        
    # 4. Non-Functional Requirements
    h1 = doc.add_heading("4. Non-Functional Requirements (NFR)", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    
    nfr_items = [
        ("NFR-01: Performance & Startup Latency", "The application MUST launch and deserialize 533k rows in under 2 seconds using Apache PyArrow Snappy Parquet caching."),
        ("NFR-02: Portability & Cross-Platform Compatibility", "The software MUST run seamlessly across macOS, Linux, and Windows 10/11 with zero OS-specific dependencies."),
        ("NFR-03: Submission Package Size Constraint", "The complete submission bundle MUST adhere to a strict <= 10.0 MB upload limit for academic and IBM portal compatibility."),
        ("NFR-04: Resilience & Self-Healing Data Pipeline", "If local cache files are absent, the application MUST automatically download, clean, and initialize the UCI dataset on-the-fly."),
        ("NFR-05: UI Responsiveness & Interactive Visuals", "All Plotly visuals MUST render asynchronously with zoom, hover tooltips, and interactive filter controls."),
        ("NFR-06: Documentation & Attribution Integrity", "The project MUST strictly preserve open-source MIT licensing and credit the foundational architectural UI layout.")
    ]
    for code, desc in nfr_items:
        p = doc.add_paragraph()
        run_code = p.add_run(code + ": ")
        run_code.bold = True
        run_code.font.color.rgb = RGBColor(14, 165, 233)
        p.add_run(desc)
        p.paragraph_format.space_after = Pt(4)
        
    # 5. Technical Requirements & Environment
    h1 = doc.add_heading("5. System Environment & Software Requirements", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    
    p = doc.add_paragraph("The required runtime environment and package dependencies are specified below:")
    
    t_sys = doc.add_table(rows=7, cols=3)
    t_sys.alignment = WD_TABLE_ALIGNMENT.CENTER
    sys_specs = [
        ("Package / Tool", "Minimum Version", "Role in Architecture"),
        ("Python", "3.10+", "Base programming runtime environment"),
        ("Streamlit", "1.30+", "Interactive C-suite web application interface"),
        ("Plotly", "5.18+", "Interactive charts, Pareto curves, and heatmaps"),
        ("Pandas & NumPy", "2.0+ / 1.24+", "Vectorized data cleaning, RFM quintiles, and aggregations"),
        ("SciPy & Scikit-Learn", "1.10+ / 1.3+", "Statistical regressions, RFM modeling, Holt-Winters forecasting"),
        ("PyArrow & OpenPyXL", "14.0+ / 3.1+", "High-speed Parquet cache serialization and Excel ingestion")
    ]
    for i, (col1, col2, col3) in enumerate(sys_specs):
        c1, c2, c3 = t_sys.rows[i].cells
        c1.text = col1
        c2.text = col2
        c3.text = col3
        if i == 0:
            set_cell_background(c1, "1E293B")
            set_cell_background(c2, "1E293B")
            set_cell_background(c3, "1E293B")
            for c in [c1, c2, c3]:
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_background(c1, "F8FAFC" if i % 2 == 1 else "FFFFFF")
            set_cell_background(c2, "F8FAFC" if i % 2 == 1 else "FFFFFF")
            set_cell_background(c3, "F8FAFC" if i % 2 == 1 else "FFFFFF")
            c1.paragraphs[0].runs[0].font.bold = True
        c1.width = Inches(2.2)
        c2.width = Inches(1.5)
        c3.width = Inches(3.3)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # 6. Verification & Run Instructions
    h1 = doc.add_heading("6. Execution & Verification Procedure", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    
    p = doc.add_paragraph("Evaluators can execute and verify the platform using standard terminal commands:")
    
    steps = [
        "Clone the repository: git clone https://github.com/hs-techlabs/ibm-project.git",
        "Navigate into directory: cd ibm-project",
        "Create virtual environment: python3 -m venv venv && source venv/bin/activate",
        "Install dependencies: pip install -r requirements.txt",
        "Launch application: streamlit run project.py",
        "Access executive dashboard in browser at: http://localhost:8501"
    ]
    for s in steps:
        p = doc.add_paragraph(s, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        
    doc.save(output_path)
    print(f"DOCX Requirements successfully saved to: {output_path}")

def create_pdf_requirements(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=1, # Center
        spaceAfter=4
    )
    
    style_sub = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4F46E5'),
        alignment=1,
        spaceAfter=15
    )
    
    style_h1 = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    style_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    style_req = ParagraphStyle(
        'ReqText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    
    story = []
    
    story.append(Paragraph("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", style_title))
    story.append(Paragraph("Vanguard: Retail Revenue & Customer Decision Intelligence Platform<br/><b>IBM Project Submission Track: Data Analytics & Applied AI</b>", style_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4F46E5'), spaceAfter=10))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Project Title</b>", style_body), Paragraph("Vanguard: Retail Decision Intelligence Platform", style_body)],
        [Paragraph("<b>Domain / Track</b>", style_body), Paragraph("IBM Applied Data Analytics & Business Intelligence", style_body)],
        [Paragraph("<b>Repository</b>", style_body), Paragraph("https://github.com/hs-techlabs/ibm-project.git", style_body)],
        [Paragraph("<b>Author / Team</b>", style_body), Paragraph("Himanshu Sharma (HS TechLabs)", style_body)],
        [Paragraph("<b>Submission Status</b>", style_body), Paragraph("Final Deliverable Release — Ready for Evaluation", style_body)]
    ]
    t_meta = Table(meta_data, colWidths=[130, 400])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & Purpose", style_h1))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) defines the structural, functional, and environment requirements "
        "for Vanguard, an enterprise-grade Decision Intelligence Platform built upon 533,878 verified transactions from "
        "the UCI Machine Learning Repository. Vanguard bridges raw transaction records and executive boardroom decisions "
        "by operationalizing the continuum: <b>Data → Information → Insights → Decisions → Actions</b>.",
        style_body
    ))
    
    # 2. Functional Requirements
    story.append(Paragraph("2. Functional Requirements (FR)", style_h1))
    frs = [
        ("FR-01: Data Ingestion & Sanitization", "Ingest 533k+ transactions, prune non-retail codes, isolate returns (InvoiceNo 'C'), reconcile guests, and cache via PyArrow."),
        ("FR-02: Executive Decision Cockpit", "Display 6 primary C-suite KPIs (Net Revenue, Gross Profit, Total Orders, AOV, Gross Margin %, Return Rate %) with period deltas."),
        ("FR-03: Revenue & Sales Velocity Module", "Render dual-axis monthly revenue versus order volume trends and intraday weekday-by-hour order density heatmap."),
        ("FR-04: Catalog & Category Intelligence", "Map SKU titles into 8 departments via keyword taxonomy and compute cumulative Pareto 80/20 SKU distribution curves."),
        ("FR-05: Algorithmic RFM Customer Segmentation", "Score accounts on Recency, Frequency, and Monetary quintiles (1-5), classifying Champions, Loyalists, and At-Risk cohorts."),
        ("FR-06: Corporate Risk & Opportunity Engine", "Quantify domestic UK revenue exposure (82.4%) and size cross-border wholesale expansion vectors ($485 international AOV)."),
        ("FR-07: Predictive Demand & Price Elasticity Simulator", "Execute Holt-Winters time-series forecasting with 95% CI and dynamic sliders for pricing and COGS inflation scenarios."),
        ("FR-08: Consolidated Single-File Architecture", "Provide single-click execution via self-contained project.py adhering strictly to IBM submission standards.")
    ]
    for code, desc in frs:
        story.append(Paragraph(f"<b><font color='#4F46E5'>{code}</font></b>: {desc}", style_req))
        
    # 3. Non-Functional Requirements
    story.append(Paragraph("3. Non-Functional Requirements (NFR)", style_h1))
    nfrs = [
        ("NFR-01: Performance & Startup Latency", "Sub-second deserialization and dashboard boot (< 2 seconds) via PyArrow Snappy Parquet caching."),
        ("NFR-02: Submission Size Compliance", "Total packaged submission archive MUST strictly not exceed 10.0 MB for portal compatibility."),
        ("NFR-03: Self-Healing Data Resilience", "Automatic fallback pipeline downloads, cleans, and generates cache if local files are missing."),
        ("NFR-04: Cross-Platform Portability", "Identical, reproducible execution across macOS, Linux, and Windows 10/11 environments.")
    ]
    for code, desc in nfrs:
        story.append(Paragraph(f"<b><font color='#0284C7'>{code}</font></b>: {desc}", style_req))
        
    # 4. System Environment & Dependencies
    story.append(Paragraph("4. System Environment & Software Dependencies", style_h1))
    env_data = [
        [Paragraph("<b>Component</b>", style_req), Paragraph("<b>Version</b>", style_req), Paragraph("<b>Architectural Role</b>", style_req)],
        [Paragraph("Python", style_req), Paragraph("3.10+", style_req), Paragraph("Core runtime environment", style_req)],
        [Paragraph("Streamlit", style_req), Paragraph("1.30+", style_req), Paragraph("Executive web application interface", style_req)],
        [Paragraph("Plotly", style_req), Paragraph("5.18+", style_req), Paragraph("Interactive time-series, Pareto curves, and heatmaps", style_req)],
        [Paragraph("Pandas & NumPy", style_req), Paragraph("2.0+ / 1.24+", style_req), Paragraph("Vectorized ETL, RFM scoring, and aggregations", style_req)],
        [Paragraph("SciPy & Scikit-Learn", style_req), Paragraph("1.10+ / 1.3+", style_req), Paragraph("Statistical regressions and Holt-Winters forecasting", style_req)],
        [Paragraph("PyArrow & OpenPyXL", style_req), Paragraph("14.0+ / 3.1+", style_req), Paragraph("High-speed Parquet cache & Excel ingestion", style_req)]
    ]
    t_env = Table(env_data, colWidths=[120, 90, 320])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_env)
    story.append(Spacer(1, 8))
    
    # 5. Quick Run Instructions
    story.append(Paragraph("5. Quick Verification & Execution", style_h1))
    story.append(Paragraph("Evaluators can verify the application with: <code>git clone https://github.com/hs-techlabs/ibm-project.git &amp;&amp; pip install -r requirements.txt &amp;&amp; streamlit run project.py</code>", style_body))
    
    doc.build(story)
    print(f"PDF Requirements successfully saved to: {output_path}")

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    
    # Generate in reports/
    docx_path = os.path.join(base, 'reports', 'Project_Requirements.docx')
    pdf_path = os.path.join(base, 'reports', 'Project_Requirements.pdf')
    create_docx_requirements(docx_path)
    create_pdf_requirements(pdf_path)
    
    # Also copy to IBM_PROJECT/
    import shutil
    shutil.copy(docx_path, os.path.join(base, 'IBM_PROJECT', 'Project_Requirements.docx'))
    shutil.copy(pdf_path, os.path.join(base, 'IBM_PROJECT', 'Project_Requirements.pdf'))
    
    # Also copy to root for instant access
    shutil.copy(docx_path, os.path.join(base, 'Project_Requirements.docx'))
    shutil.copy(pdf_path, os.path.join(base, 'Project_Requirements.pdf'))
    print("All requirements files generated and distributed!")
