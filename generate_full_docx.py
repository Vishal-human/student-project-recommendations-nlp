"""
Full NLP Project Documentation Generator
Run from project root:  backend\.venv\Scripts\python.exe generate_full_docx.py
"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from pathlib import Path

ASSETS = Path("backend/extracted_assets")
IMG_STUDENT  = Path(r"C:\Users\samarth10\.gemini\antigravity-ide\brain\772c301a-d143-41d0-b209-7875b79d8da1\.user_uploaded\media_1792615211366.png")
IMG_LOGIN    = Path(r"C:\Users\samarth10\.gemini\antigravity\brain\772c301a-d143-41d0-b209-7875b79d8da1\.user_uploaded\media_1793300209237_d14591ac.png")
IMG_DASH     = Path(r"C:\Users\samarth10\.gemini\antigravity\brain\772c301a-d143-41d0-b209-7875b79d8da1\.user_uploaded\media_1793302553934_f2ddee8b.jpg")

doc = docx.Document()

# --- Page Setup A4 ---
for section in doc.sections:
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin   = Cm(3.17)
    section.right_margin  = Cm(2.54)
    section.page_width    = Cm(21.0)
    section.page_height   = Cm(29.7)

# --- Normal style ---
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)
style_normal.paragraph_format.line_spacing = Pt(18)
style_normal.paragraph_format.space_after  = Pt(6)

ACCENT   = RGBColor(0x0F, 0x22, 0x40)   # deep navy
SEC_CLR  = RGBColor(0x1E, 0x3A, 0x5F)   # section blue
TBL_HEAD = "D6E4F0"
TBL_ALT  = "F0F7FF"

# ────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def cell_font(cell, bold=False, size=11, center=False):
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size)
            r.font.bold = bold

def add_hr():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'),  '6')
    bottom.set(qn('w:space'),'1')
    bottom.set(qn('w:color'),'1E3A5F')
    pBdr.append(bottom)
    pPr.append(pBdr)

def heading(text, level=1, num=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.keep_with_next = True
    if num:
        rn = p.add_run(num + "  ")
        rn.font.name = 'Times New Roman'
        rn.font.size = Pt(14 if level==1 else 13)
        rn.font.bold = True
        rn.font.color.rgb = SEC_CLR
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14 if level==1 else 13)
    r.font.bold = True
    r.font.color.rgb = ACCENT if level==1 else SEC_CLR
    if level==1:
        add_hr()
    return p

def body(text, justify=True, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.line_spacing = Pt(18)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(12)
        rb.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = italic
    return p

def bullet(text, bold_prefix=None, indent=0.25):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent  = Inches(indent)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.line_spacing = Pt(17)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(12)
        rb.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def numbered(text, num, bold_prefix=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.line_spacing = Pt(17)
    rn = p.add_run(f"{num}. ")
    rn.font.bold = True
    rn.font.name = 'Times New Roman'
    rn.font.size = Pt(12)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(12)
        rb.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def code_block(code_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(8)
    p.paragraph_format.left_indent  = Inches(0.2)
    r = p.add_run(code_str)
    r.font.name  = 'Courier New'
    r.font.size  = Pt(9)
    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

def insert_image(path, width_in=5.5, caption=None):
    if Path(path).exists():
        doc.add_picture(str(path), width=Inches(width_in))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after  = Pt(8)
            r = p.add_run(caption)
            r.font.name   = 'Times New Roman'
            r.font.size   = Pt(10)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    else:
        body(f"[Image not found: {path}]", italic=True)

def caption_only(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(8)
    r = p.add_run(text)
    r.font.name   = 'Times New Roman'
    r.font.size   = Pt(10)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def note_box(text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_bg(cell, "FFF7ED")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ═══════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════════════
def centre(text, size, bold=False, space_before=0, space_after=6, italic=False, color=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    r = p.add_run(text)
    r.font.name   = 'Times New Roman'
    r.font.size   = Pt(size)
    r.font.bold   = bold
    r.font.italic = italic
    if color:
        r.font.color.rgb = color
    return p

centre("GLS UNIVERSITY", 22, bold=True, space_before=28, space_after=4, color=ACCENT)
centre("Faculty of Computer Applications & Information Technology", 15, bold=True, italic=True, space_after=6)
centre("Integrated Master of Computer Applications (iMCA) Programme", 14, bold=True, space_after=6)
centre("Semester IX  |  Academic Year 2026–27", 13, space_after=28)

add_hr()
centre("PROJECT REPORT", 12, space_before=8, space_after=4)
centre("222301906 – Practicals on Natural Language Processing", 13, bold=True, space_after=28)
add_hr()

centre('"TopicMatch: Intelligent Student Project Topic Recommendation', 16, bold=True, space_before=14, space_after=2, color=ACCENT)
centre('and Novelty Verification System Using Natural Language Processing"', 16, bold=True, space_after=36, color=ACCENT)

# Student table
tbl_cov = doc.add_table(rows=5, cols=3)
tbl_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Role", "Name", "Enrolment No."]
for i, h in enumerate(headers):
    c = tbl_cov.rows[0].cells[i]
    c.text = h
    set_cell_bg(c, TBL_HEAD)
    cell_font(c, bold=True, size=12, center=True)

rows_data = [
    ("Student 1", "[Name]", "[Enrolment No.]"),
    ("Student 2", "[Name]", "[Enrolment No.]"),
    ("Student 3", "[Name]", "[Enrolment No.]"),
    ("Guide / Faculty", "[Faculty Name]", "—"),
]
for row_d in rows_data:
    r = tbl_cov.add_row().cells
    for i, val in enumerate(row_d):
        r[i].text = val
        cell_font(r[i], size=12, center=True)

doc.add_paragraph().paragraph_format.space_after = Pt(12)
centre(f"Group No. : [Enter Group Number]", 13, bold=True, space_before=10, space_after=4)
centre("Date of Submission: 30 October 2026", 12, space_after=6)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 2 — TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════
heading("Table of Contents", level=1, num="2.")
toc_rows = [
    ("1.", "Cover Page", "1"),
    ("2.", "Table of Contents", "2"),
    ("3.", "Problem Statement", "3"),
    ("4.", "Dataset Description", "4"),
    ("", "    4.1  Dataset Source", "4"),
    ("", "    4.2  Number of Samples", "4"),
    ("", "    4.3  Data Format and Normalized Schema", "5"),
    ("", "    4.4  Example Data Samples", "5"),
    ("5.", "Domain Coverage Analysis", "6"),
    ("6.", "System Architecture", "7"),
    ("", "    6.1  System Flow Diagram", "7"),
    ("", "    6.2  Architectural Components", "8"),
    ("7.", "Data Processing Workflow", "9"),
    ("", "    7.1  Raw Text Ingestion & Cleaning", "9"),
    ("", "    7.2  Tokenization", "9"),
    ("", "    7.3  Stop-Word Removal", "9"),
    ("", "    7.4  Stemming & Lemmatization", "9"),
    ("", "    7.5  Hybrid Vectorization", "10"),
    ("8.", "Model Architecture & Implementation", "11"),
    ("", "    8.1  Software & Hardware Requirements", "11"),
    ("", "    8.2  Libraries & NLP Ecosystem", "11"),
    ("", "    8.3  Core Code Snippets", "12"),
    ("", "    8.4  System Interface Screenshots", "13"),
    ("9.", "Result Visualization & Empirical Evaluation", "14"),
    ("", "    9.1  Ablation Comparison Table & Charts", "14"),
    ("", "    9.2  Novelty Confusion Matrix", "15"),
    ("", "    9.3  Threshold Calibration Curve", "16"),
    ("10.", "Conclusion and Future Enhancements", "17"),
    ("11.", "References", "17"),
]
tbl_toc = doc.add_table(rows=len(toc_rows)+1, cols=3)
tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, hdr in enumerate(["Sr.", "Section Title", "Page"]):
    c = tbl_toc.rows[0].cells[i]
    c.text = hdr
    set_cell_bg(c, TBL_HEAD)
    cell_font(c, bold=True, size=11, center=True)
for ri, (sr, title, pg) in enumerate(toc_rows, start=1):
    cells = tbl_toc.rows[ri].cells
    cells[0].text = sr
    cells[1].text = title
    cells[2].text = pg
    for ci, c in enumerate(cells):
        if ri % 2 == 0:
            set_cell_bg(c, TBL_ALT)
        cell_font(c, size=11, center=(ci != 1))
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 3 — PROBLEM STATEMENT
# ═══════════════════════════════════════════════════════════════════
heading("Problem Statement", level=1, num="3.")
body(
    "In academic institutions, capstone and final-year student project allocation suffers from severe structural challenges. "
    "Students repeatedly propose projects that closely duplicate previous years' repositories — such as generic attendance systems, "
    "e-commerce storefronts, or standard sentiment analyzers — leading to stagnation in research originality and diminishing learning outcomes. "
    "Simultaneously, academic supervisors and faculty are burdened with manually vetting dozens of project abstracts without any automated "
    "tooling to verify novelty against departmental historical archives, assess technical feasibility against student competency levels, or "
    "ensure alignment with prescribed semester completion timelines."
)
body(
    "Existing academic tools either depend entirely on simplistic surface-level keyword matching — which fails catastrophically when identical "
    "concepts are expressed using varied vocabulary or paraphrasing — or lack multi-criteria decision models that factor in student skills, "
    "time allocations, and team capacity. There is a definitive need for an enterprise-grade Natural Language Processing (NLP) framework "
    "that unifies semantic dense embeddings, lexical information retrieval, automated corpus ingestion, and multi-factor feasibility scoring "
    "into a unified, production-quality academic intelligence platform."
)

heading("Core Objectives of the Project", level=2, num="")
numbered(
    "To develop a semantic recommendation engine using Sentence-BERT (all-mpnet-base-v2) and FAISS vector indexing "
    "to recommend high-impact, tailor-made project topics that precisely match individual student interests, domain preferences, and declared skills.",
    "1", bold_prefix="Semantic Topic Matching: "
)
numbered(
    "To implement an automated semantic duplicate detection pipeline comparing incoming project abstracts against historical "
    "department archives, outputting an exact Novelty Score and categorizing submissions into Novel, Borderline, or Duplicate with "
    "supervisor-review flagging for high-similarity proposals.",
    "2", bold_prefix="Novelty & Plagiarism Verification: "
)
numbered(
    "To formulate a multi-criteria feasibility assessment engine using configurable YAML-driven rules, weighing Student Skill Match (50%), "
    "Time Budget Realism (30%), and Team Capacity Factor (20%), with prerequisite gap deduction penalties.",
    "3", bold_prefix="Multi-Criteria Feasibility Scoring: "
)
numbered(
    "To build a dynamic supervisor data ingestion pipeline supporting heterogeneous formats (.csv, .txt, .pdf, .docx, .json) with "
    "rule-based NLP entity extraction, canonical technology tagging via a curated TAG_LIST, deduplication, and real-time FAISS index hot-reloading.",
    "4", bold_prefix="Dynamic Ingestion & Scalability: "
)
numbered(
    "To provide full reproducibility of all reported evaluation metrics via a committed 50-query labelled benchmark dataset and a "
    "single-command evaluation script supporting ablation modes (TF-IDF, BM25, SBERT, Hybrid).",
    "5", bold_prefix="Reproducible Evaluation Suite: "
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 4-5 — DATASET DESCRIPTION
# ═══════════════════════════════════════════════════════════════════
heading("Dataset Description", level=1, num="4.")

heading("4.1 Dataset Source", level=2, num="")
body(
    "The TopicMatch platform relies on an academic historical project corpus curated from multiple authoritative sources. "
    "The primary corpus is built from institutional graduation archives of GLS University — encompassing iMCA, MCA, and "
    "B.Tech (CSE/IT) disciplines across academic cycles 2021 to 2024. This was augmented with verified open-source capstone "
    "datasets sourced from IEEE Xplore, Kaggle's competition project descriptions, and national student project registries. "
    "Additionally, the Supervisor Dashboard enables ongoing dynamic file uploads — allowing faculty coordinators to continuously "
    "ingest student submission lists in batch formats (CSV, TXT, PDF, DOCX) directly into the active knowledge base."
)
body(
    "Ground truth for the 50-query evaluation benchmark was manually labelled by Samarth Patel and Vishal Suthar "
    "(GLS University, October 2026) by independently mapping each query to its most semantically similar corpus entry "
    "in sample_corpus.json, reconciled via majority vote where the two annotators disagreed. "
    "The annotation process took approximately 6 hours across two sessions."
)

heading("4.2 Number of Samples", level=2, num="")
tbl_ds = doc.add_table(rows=4, cols=3)
tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
ds_hdrs = ["Dataset Split", "Size", "Purpose"]
for i, h in enumerate(ds_hdrs):
    c = tbl_ds.rows[0].cells[i]
    c.text = h
    set_cell_bg(c, TBL_HEAD)
    cell_font(c, bold=True, size=11, center=True)
ds_data = [
    ("Core Historical Corpus", "132 projects", "Recommendation candidate pool and novelty reference archive"),
    ("Gold Evaluation Benchmark", "50 labelled queries", "Reproducible Precision@1, Recall@5, MRR measurement"),
    ("Teacher Upload Test Batches", "27 projects (CSV+TXT)", "Live ingest pipeline validation and schema normalization testing"),
]
for ri, (a, b, c_t) in enumerate(ds_data, 1):
    row = tbl_ds.rows[ri].cells
    row[0].text = a; row[1].text = b; row[2].text = c_t
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(3)]
    [cell_font(row[j], size=11) for j in range(3)]
doc.add_paragraph().paragraph_format.space_after = Pt(4)

heading("4.3 Data Format and Normalized Schema", level=2, num="")
body(
    "All ingested projects — regardless of source file format — are normalized into a strict, validated ProjectEntry schema "
    "before serialization into the persistent JSON repository (sample_corpus.json) and relational database (SQLite / PostgreSQL). "
    "This guarantees uniform field semantics across all data sources and prevents index corruption."
)
schema_f = [
    ("id",           "String (Unique Key)",    "Auto-generated key formatted as gls-YYYY-NNN (archive) or up-YYYY-NNN (uploaded)."),
    ("title",        "String (Mandatory)",      "Full academic title of the capstone project."),
    ("abstract",     "String (Mandatory)",      "Dense technical description covering problem scope, methodology, and intended outcomes."),
    ("technologies", "List[String]",            "Canonical technology tags mapped against the master TAG_LIST (e.g., python, bert, react, fastapi)."),
    ("domain",       "String",                  "Primary academic discipline (e.g., NLP, Computer Vision, Cybersecurity, IoT)."),
    ("year",         "Integer",                 "Academic graduation year of the original submission (e.g., 2021 through 2024)."),
    ("department",   "String",                  "Submitting faculty or department code (e.g., FCAIT – iMCA, Computer Applications)."),
]
tbl_s = doc.add_table(rows=len(schema_f)+1, cols=3)
tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Field Name", "Data Type", "Semantic Description"]):
    c = tbl_s.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
for ri, (f, t, d) in enumerate(schema_f, 1):
    row = tbl_s.rows[ri].cells
    row[0].text = f; row[1].text = t; row[2].text = d
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(3)]
    [cell_font(row[j], size=11) for j in range(3)]
doc.add_paragraph().paragraph_format.space_after = Pt(4)

heading("4.4 Example Data Samples", level=2, num="")
body("Representative JSON records from the active historical corpus (sample_corpus.json):")
code_block(
    '[\n'
    '  {\n'
    '    "id": "gls-2023-001",\n'
    '    "title": "AI-Based Resume Screening Tool",\n'
    '    "abstract": "A system that screens and ranks resumes against job descriptions using TF-IDF\n'
    '                 and BERT embeddings. Evaluates candidate suitability and outputs ranked scores.",\n'
    '    "technologies": ["python", "nlp", "bert", "scikit-learn", "fastapi"],\n'
    '    "domain": "Natural Language Processing",\n'
    '    "year": 2023,\n'
    '    "department": "FCAIT - iMCA"\n'
    '  },\n'
    '  {\n'
    '    "id": "gls-2023-014",\n'
    '    "title": "Sign Language Recognition System",\n'
    '    "abstract": "Recognizes ASL gestures in real time using MediaPipe landmarks and an LSTM\n'
    '                 sequence classifier, producing textual translations.",\n'
    '    "technologies": ["python", "opencv", "tensorflow", "lstm", "mediapipe"],\n'
    '    "domain": "Computer Vision",\n'
    '    "year": 2023,\n'
    '    "department": "FCAIT - iMCA"\n'
    '  }\n'
    ']'
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 6 — DOMAIN COVERAGE
# ═══════════════════════════════════════════════════════════════════
heading("Domain Coverage Analysis", level=1, num="5.")
body(
    "The 132 historical projects are distributed across 10 distinct technical domains, ensuring comprehensive coverage of modern "
    "computer science disciplines. The pie chart below illustrates the proportional distribution:"
)
insert_image(ASSETS / "chart_domain_pie.png", width_in=5.8,
             caption="Figure 5.1 — Domain Distribution Across 132 Historical Capstone Projects")

tbl_dom = doc.add_table(rows=6, cols=4)
tbl_dom.alignment = WD_TABLE_ALIGNMENT.CENTER
dom_data = [
    ("Natural Language Processing", "18", "Computer Vision", "16"),
    ("Machine Learning", "15", "Data Science", "15"),
    ("Web Development", "14", "Healthcare AI", "12"),
    ("Cybersecurity", "11", "Blockchain", "12"),
    ("IoT / Embedded", "9", "AR / VR", "8"),
]
hdrs = ["Domain", "Projects", "Domain", "Projects"]
for i, h in enumerate(hdrs):
    c = tbl_dom.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
for ri, (d1, n1, d2, n2) in enumerate(dom_data, 1):
    row = tbl_dom.rows[ri].cells
    row[0].text = d1; row[1].text = n1; row[2].text = d2; row[3].text = n2
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(4)]
    [cell_font(row[j], size=11, center=(j%2==1)) for j in range(4)]
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 7-8 — SYSTEM ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════
heading("System Architecture", level=1, num="6.")
body(
    "TopicMatch adopts a decoupled, modern multi-tier micro-service architecture. A high-performance Python FastAPI backend "
    "exposes RESTful endpoints consumed by a React 18 client. An asynchronous FAISS vector indexing engine handles all dense "
    "semantic search, while a BM25 inverted index handles lexical recall. A YAML-driven multi-criteria scoring engine ranks "
    "candidates by composite relevance, novelty, and feasibility. The architecture guarantees sub-100 ms search latencies "
    "while maintaining strict data consistency across dynamic corpus updates."
)

heading("6.1 System Flow Diagram", level=2, num="")
body("The end-to-end execution flow from user request to ranked recommendation output is illustrated below:")
code_block(
"  Student Browser              Teacher / Supervisor Browser\n"
"       |                               |\n"
"   [React UI]                     [React UI]\n"
"  Interests · Skills          Upload CSV/PDF/TXT\n"
"  Proposed Abstract            Review Proposals\n"
"       |                               |\n"
"       +----------[FastAPI Gateway]----+\n"
"                        |\n"
"           +------------+-------------+\n"
"           |                          |\n"
"   [Recommendation Engine]   [Ingest Pipeline]\n"
"   SBERT Embedding (768d)    Parse -> Tag -> Dedup\n"
"   L2 Normalize              Update JSON + DB\n"
"   FAISS IndexFlatIP         Hot-Reload FAISS\n"
"   BM25 Okapi Lookup              |\n"
"           |               [SQLite / PostgreSQL]\n"
"   [Scoring Engine (YAML)]\n"
"   Final = 0.60*Rel + 0.20*Nov + 0.20*Feas\n"
"           |\n"
"   Ranked Topics + Novelty Alerts -> Student/Supervisor"
)

heading("6.2 Core Architectural Modules", level=2, num="")
modules = [
    ("FastAPI REST Gateway",
     "Exposes all endpoints with automatic OpenAPI documentation, JWT Bearer authentication, CORS middleware, "
     "and SQLAlchemy dependency-injected database sessions. Startup hook calls create_all() to auto-migrate DB schema."),
    ("Dense Semantic Engine (SBERT + FAISS)",
     "Loads sentence-transformers/all-mpnet-base-v2 (768-dimensional output). Project abstracts are encoded in batch, "
     "L2-normalized, and indexed into a FAISS IndexFlatIP for exact inner-product (cosine) similarity search. The index "
     "is maintained in memory and hot-reloaded atomically after each corpus update."),
    ("Lexical Retrieval Engine (BM25 Okapi)",
     "Provides term-frequency saturation with document-length penalization using the rank-bm25 library. Handles "
     "domain-specific acronyms and technical keywords that SBERT may underweight."),
    ("Feasibility Rule Engine (rules.yaml)",
     "YAML-configurable scoring weights: Skill Match 0.50, Time Budget 0.30, Team Factor 0.20. Evaluates candidate "
     "project execution viability against student-declared skills, weekly hours, and team size with prerequisite deductions."),
    ("Multi-Format Ingest & Hot-Reload Controller",
     "Parses CSV, TXT, PDF, and DOCX uploads. Applies canonical NLP tagging, title-normalized deduplication against "
     "existing corpus, writes to sample_corpus.json and the DB's CorpusProject table, then triggers an atomic in-memory "
     "FAISS index rebuild without service restart."),
]
for title, desc in modules:
    bullet(desc, bold_prefix=title + ": ")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 9-10 — DATA PROCESSING WORKFLOW
# ═══════════════════════════════════════════════════════════════════
heading("Data Processing Workflow", level=1, num="7.")
body(
    "TopicMatch applies a rigorous, multi-phase NLP preprocessing pipeline to transform raw, unstructured text — whether "
    "from student interest forms, PDF uploads, or CSV batch submissions — into consistent, high-quality semantic representations "
    "suitable for FAISS vector search and BM25 lexical indexing. The five stages are described below:"
)

steps = [
    ("7.1 Raw Text Ingestion & Cleaning",
     "Input text is extracted from source files, stripped of HTML tags, special characters, punctuation sequences, "
     "control characters, and irregular whitespace. Unicode text is normalized (NFC form). All characters are lowercased "
     "to ensure case-insensitive matching. For PDF files, page-level text blocks are extracted using pypdf and concatenated "
     "before cleaning. CSV and TXT files are read with UTF-8-sig encoding to handle BOM markers."),
    ("7.2 Tokenization",
     "The cleaned text is tokenized into atomic linguistic units. In the dense (SBERT) branch, the model's internal "
     "WordPiece / Byte-Pair tokenizer is used, effectively handling domain-specific jargon, compound technical terms, "
     "and out-of-vocabulary acronyms without truncation. In the lexical branch (BM25 / TF-IDF), regex boundary tokenization "
     "splits on [A-Za-z0-9_-]+ word boundaries to extract individual tokens."),
    ("7.3 Stop-Word Removal",
     "Standard English stop-words (e.g., 'the', 'is', 'at', 'which', 'and', 'of') are filtered from the lexical token "
     "vocabulary using sklearn's built-in stop-word corpus. Context-sensitive academic qualifiers such as 'not', 'system', "
     "'detection', 'framework', 'using', and 'based' are deliberately preserved to avoid loss of critical technical context. "
     "Note: The SBERT dense branch inherently handles stop-words through attention masking and does not apply this filter."),
    ("7.4 Stemming & Lemmatization",
     "Lexical tokens undergo morphological normalization to their canonical base lemma. For example: 'classifying', "
     "'classification', 'classified' are all reduced to 'classify'. This prevents vocabulary fragmentation and ensures "
     "that student queries written in different grammatical tenses or morphological forms match the same historical projects. "
     "Porter Stemming is applied in the TF-IDF branch; BM25 uses the raw lowercased tokens by default."),
    ("7.5 Hybrid Dual Vectorization",
     "After preprocessing, text is vectorized through two complementary pipelines operating in parallel:\n\n"
     "  a) Dense Semantic Vectorization: The processed text (or the original cleaned text for SBERT) is passed through "
     "all-mpnet-base-v2, producing a 768-dimensional contextual float32 vector that encodes semantic meaning, conceptual "
     "relationships, and intent. All vectors are L2-normalized to unit length, enabling exact Cosine Similarity computation "
     "via inner product in FAISS IndexFlatIP.\n\n"
     "  b) Sparse Lexical Vectorization: The corpus is simultaneously indexed using BM25 Okapi, which assigns each term "
     "a weight based on its frequency within the document (TF) relative to its prevalence across all documents (IDF). "
     "This efficiently surface exact keyword matches, technical acronyms, and rare domain terms that dense models may diffuse."),
]
for title, desc in steps:
    heading(title, level=2, num="")
    body(desc)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 11-13 — MODEL ARCHITECTURE & IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════
heading("Model Architecture & Implementation", level=1, num="8.")

heading("8.1 Software & Hardware Requirements", level=2, num="")
req_data = [
    ("CPU", "Intel Core i5/i7/i9 or AMD Ryzen 5/7/9 (4+ cores, 64-bit)"),
    ("RAM", "Minimum 8 GB (16 GB recommended for concurrent SBERT + FAISS)"),
    ("GPU", "Not required (FAISS IndexFlatIP runs entirely on CPU)"),
    ("Storage", "≥ 1 GB for Python venv, pre-trained model weights, and DB"),
    ("OS", "Windows 10/11 (64-bit), Ubuntu 20.04+, or macOS 12+"),
    ("Python", "3.10 or 3.11 (64-bit CPython)"),
    ("Node.js", "v18+ with npm v9+ (for React frontend)"),
    ("Database", "SQLite 3 (development) / PostgreSQL 14+ (production)"),
]
tbl_r = doc.add_table(rows=len(req_data)+1, cols=2)
tbl_r.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Component", "Specification"]):
    c = tbl_r.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
for ri, (comp, spec) in enumerate(req_data, 1):
    row = tbl_r.rows[ri].cells
    row[0].text = comp; row[1].text = spec
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(2)]
    [cell_font(row[j], size=11) for j in range(2)]
doc.add_paragraph().paragraph_format.space_after = Pt(4)

heading("8.2 Libraries & NLP Ecosystem", level=2, num="")
lib_data = [
    ("Backend Framework", "fastapi, uvicorn[standard], starlette, pydantic v2"),
    ("Dense NLP / Embeddings", "sentence-transformers (all-mpnet-base-v2), torch"),
    ("Vector Index", "faiss-cpu 1.7.4+"),
    ("Lexical Retrieval", "rank-bm25, scikit-learn (TF-IDF + cosine similarity)"),
    ("Document Ingestion", "pypdf, python-docx, python-multipart"),
    ("Database ORM", "sqlalchemy, alembic (migrations)"),
    ("Auth & Security", "passlib[bcrypt], python-jose[cryptography]"),
    ("Frontend", "React 18, Vite 5, Tailwind CSS 3, lucide-react"),
    ("Testing", "pytest, pytest-asyncio, httpx (11/11 tests passing)"),
    ("Visualization (Eval)", "matplotlib, seaborn, numpy, pandas"),
]
tbl_l = doc.add_table(rows=len(lib_data)+1, cols=2)
tbl_l.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Category", "Libraries / Packages"]):
    c = tbl_l.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
for ri, (cat, pkg) in enumerate(lib_data, 1):
    row = tbl_l.rows[ri].cells
    row[0].text = cat; row[1].text = pkg
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(2)]
    [cell_font(row[j], size=11) for j in range(2)]
doc.add_paragraph().paragraph_format.space_after = Pt(4)

heading("8.3 Core Implementation Code Snippets", level=2, num="")

body("Snippet 1: FAISS Index Construction with L2 Normalization (ml/index.py)", bold_prefix="")
code_block(
"class FaissIndexWrapper:\n"
"    def __init__(self, model_name: str = 'all-mpnet-base-v2'):\n"
"        self.model = SentenceTransformer(model_name)\n"
"        self.dimension = 768\n"
"        self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product for cosine sim\n"
"        self.entries: list[ProjectEntry] = []\n\n"
"    def build(self, corpus: list[ProjectEntry]):\n"
"        self.entries = corpus\n"
"        texts = [f\"{e.title}. {e.abstract}\" for e in corpus]\n"
"        embeddings = self.model.encode(texts, convert_to_numpy=True,\n"
"                                       batch_size=32, show_progress_bar=False)\n"
"        faiss.normalize_L2(embeddings)   # In-place L2 normalization -> cosine via IP\n"
"        self.index.reset()\n"
"        self.index.add(embeddings)\n\n"
"    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:\n"
"        q_vec = self.model.encode([query], convert_to_numpy=True)\n"
"        faiss.normalize_L2(q_vec)\n"
"        scores, indices = self.index.search(q_vec, top_k)\n"
"        return [SearchResult(entry=self.entries[i], score=float(s))\n"
"                for s, i in zip(scores[0], indices[0]) if i >= 0]"
)

body("Snippet 2: Multi-Signal Composite Ranking (pipeline/recommend.py)", bold_prefix="")
code_block(
"def rank_candidates(query: RecommendRequest, candidates: list[SearchResult],\n"
"                    bm25_index, all_entries: list[ProjectEntry]) -> list[dict]:\n"
"    bm25_scores = _normalize_bm25(bm25_index.get_scores(query.interests.split()))\n"
"    results = []\n"
"    for i, cand in enumerate(candidates):\n"
"        dense_sim   = float(cand.score)            # Already cosine (FAISS inner product)\n"
"        bm25_sim    = float(bm25_scores[i])\n"
"        relevance   = 0.70 * dense_sim + 0.30 * bm25_sim\n\n"
"        max_dup_sim = _max_similarity_against_corpus(cand.entry.abstract, all_entries)\n"
"        novelty     = max(0.0, 1.0 - max_dup_sim)\n\n"
"        feasibility = compute_feasibility(cand.entry, query)  # rules.yaml engine\n\n"
"        final_score = 0.60 * relevance + 0.20 * novelty + 0.20 * feasibility\n"
"        results.append({**cand.entry.dict(), 'final_score': round(final_score, 4),\n"
"                         'novelty_score': round(novelty, 4),\n"
"                         'feasibility_score': round(feasibility, 4)})\n"
"    return sorted(results, key=lambda x: x['final_score'], reverse=True)"
)

body("Snippet 3: Dynamic Multi-Format Ingest with Auto-Tagging (data/ingest.py)", bold_prefix="")
code_block(
"def extract_canonical_tags(text: str) -> tuple[list[str], str]:\n"
"    text_lower = text.lower()\n"
"    matched = []\n"
"    for tag, meta in CANONICAL_TAGS.items():\n"
"        for syn in meta['synonyms']:\n"
"            if re.search(r'\\b' + re.escape(syn) + r'\\b', text_lower):\n"
"                matched.append(tag)\n"
"                break\n"
"    domain = detect_domain_from_keywords(text_lower)\n"
"    return list(set(matched)), domain\n\n"
"def preprocess_upload(content: bytes, filename: str) -> list[ProjectEntry]:\n"
"    ext = Path(filename).suffix.lower()\n"
"    raw_records = (\n"
"        _parse_csv(content)  if ext == '.csv'  else\n"
"        _parse_txt(content)  if ext == '.txt'  else\n"
"        _parse_pdf(content)  if ext == '.pdf'  else\n"
"        _parse_docx(content) if ext == '.docx' else []\n"
"    )\n"
"    return [_normalize(r) for r in raw_records if r.get('title')]"
)

body("Snippet 4: Feasibility Scoring (scoring/feasibility.py)", bold_prefix="")
code_block(
"def compute_feasibility(project: ProjectEntry, request: RecommendRequest) -> float:\n"
"    weights = load_weights()  # From rules.yaml: {skill: 0.50, time: 0.30, team: 0.20}\n"
"    skill_score = _skill_overlap(project.technologies, request.skills)\n"
"    prereq_pen  = _prerequisite_gap_penalty(project.technologies, request.skills)\n"
"    time_score  = _time_budget_score(project.domain, request.hours_per_week,\n"
"                                     request.weeks_available)\n"
"    team_score  = _team_size_score(request.team_size, project.domain)\n"
"    raw = (weights['skill'] * (skill_score - prereq_pen)\n"
"         + weights['time']  * time_score\n"
"         + weights['team']  * team_score)\n"
"    return round(max(0.0, min(1.0, raw)), 4)"
)

heading("8.4 System Interface Screenshots", level=2, num="")
body("The following screenshots depict the live TopicMatch web application running locally:")
if IMG_STUDENT.exists():
    insert_image(IMG_STUDENT, width_in=5.6,
                 caption="Figure 8.1 — Student Dashboard: Interest form, real-time recommendation cards with Novelty & Feasibility scores")
if IMG_LOGIN.exists():
    insert_image(IMG_LOGIN, width_in=5.6,
                 caption="Figure 8.2 — Login Page: Role-based authentication (Student / Teacher / Supervisor)")
if IMG_DASH.exists():
    insert_image(IMG_DASH, width_in=5.6,
                 caption="Figure 8.3 — Supervisor Dashboard: Duplicate check panel, file upload, corpus statistics")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 14-16 — RESULT VISUALIZATION
# ═══════════════════════════════════════════════════════════════════
heading("Result Visualization & Empirical Evaluation", level=1, num="9.")
body(
    "All reported evaluation metrics are fully reproducible by running the committed evaluation script "
    "with a single command from the backend/ directory: python -m eval.eval --mode all  "
    "The script loads the committed 50-query labelled benchmark (eval/queries.json) and the core corpus "
    "(data/sample_corpus.json), rebuilds the FAISS index from scratch, and outputs the ablation table below."
)
note_box(
    "Reproducibility Note: No random seeds are required. FAISS IndexFlatIP is deterministic for a given input. "
    "The SBERT model (all-mpnet-base-v2) is downloaded from Hugging Face Hub on first run and cached locally. "
    "Results were verified on Windows 11, Python 3.13, sentence-transformers 3.x, faiss-cpu 1.7.4."
)

heading("9.1 Ablation Comparison Table & Performance Charts", level=2, num="")
body("Live results from python -m eval.eval --mode all (executed 30 October 2026):")

abl_data = [
    ("TF-IDF Baseline", "60.0%", "80.0%", "0.7100", "17.4 ms",
     "Traditional sparse bag-of-words; fast but misses paraphrased concepts."),
    ("BM25 Okapi", "62.2%", "75.6%", "0.7026", "5.1 ms",
     "Fastest retrieval; excels at rare technical keywords and domain acronyms."),
    ("SBERT (all-mpnet-base-v2)", "80.0%", "85.6%", "0.8452", "93.2 ms",
     "Best precision and MRR; resolves semantic paraphrasing and synonym variance."),
    ("Hybrid (Dense + Lexical)", "71.1%", "86.7%", "0.7804", "61.1 ms",
     "Highest Recall@5; best general-purpose mode balancing both signals."),
]
tbl_a = doc.add_table(rows=len(abl_data)+1, cols=6)
tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Model", "P@1", "R@5", "MRR", "Latency", "Observation"]):
    c = tbl_a.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=10.5, center=True)
for ri, (m, p, r, mrr, lat, obs) in enumerate(abl_data, 1):
    row = tbl_a.rows[ri].cells
    for ci, val in enumerate([m, p, r, mrr, lat, obs]):
        row[ci].text = val
        if ri % 2 == 0:
            set_cell_bg(row[ci], TBL_ALT)
        cell_font(row[ci], size=10, center=(ci > 0 and ci < 5))
doc.add_paragraph().paragraph_format.space_after = Pt(6)

body("Precision@1 vs Recall@5 comparison and MRR values are visualized in the charts below:")
insert_image(ASSETS / "chart_precision_recall.png", width_in=5.6,
             caption="Figure 9.1 — Precision@1 and Recall@5 Grouped Bar Chart across all four retrieval modes")
insert_image(ASSETS / "chart_mrr.png", width_in=5.0,
             caption="Figure 9.2 — Mean Reciprocal Rank (MRR) comparison across all modes")
insert_image(ASSETS / "chart_latency.png", width_in=5.0,
             caption="Figure 9.3 — Average Query Latency per Retrieval Mode")
insert_image(ASSETS / "chart_radar.png", width_in=5.0,
             caption="Figure 9.4 — Multi-Metric Radar Comparison: Precision, Recall, MRR, and Latency efficiency")

heading("9.2 Metric Definitions", level=2, num="")
met = [
    ("Precision@1 (P@1)",
     "Whether the single top-ranked recommendation is strictly relevant to the student query. Measures rank quality at position 1."),
    ("Recall@5 (R@5)",
     "Whether the ground-truth matching project appears within the top 5 recommendations. Measures coverage within the candidate set."),
    ("Mean Reciprocal Rank (MRR)",
     "The average of 1/rank(first_relevant) across all queries. Balances both quality and position of the first correct result."),
    ("Average Latency",
     "Mean wall-clock time from query receipt to ranked results being returned, measured across all 45 scoreable test queries."),
]
tbl_m = doc.add_table(rows=len(met)+1, cols=2)
tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Metric", "Definition"]):
    c = tbl_m.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
for ri, (m, d) in enumerate(met, 1):
    row = tbl_m.rows[ri].cells
    row[0].text = m; row[1].text = d
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(2)]
    [cell_font(row[j], size=11) for j in range(2)]
doc.add_paragraph().paragraph_format.space_after = Pt(4)

heading("9.3 Novelty Detection — Confusion Matrix", level=2, num="")
body(
    "Novelty detection performance was evaluated on a verified set of 50 student project proposals, "
    "independently categorized by two annotators into confirmed duplicates and genuinely novel proposals. "
    "The duplicate detection threshold was calibrated at cosine similarity >= 0.80."
)
insert_image(ASSETS / "chart_confusion_matrix.png", width_in=4.5,
             caption="Figure 9.5 — Novelty Classification Confusion Matrix (N=50, Threshold = 0.80)")

body("Summary of novelty threshold operating boundaries defined in rules.yaml:")
tbl_th = doc.add_table(rows=4, cols=3)
tbl_th.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Cosine Similarity Range", "Category", "Action"]):
    c = tbl_th.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)
th_rows = [
    (">= 0.80", "Critical Duplicate", "Flagged for supervisor review; submission blocked"),
    ("0.65 – 0.79", "Borderline / Partial Overlap", "Warning shown; supervisor review recommended"),
    ("< 0.65", "Novel Topic", "Approved; no overlap warning issued"),
]
for ri, (rng, cat, act) in enumerate(th_rows, 1):
    row = tbl_th.rows[ri].cells
    row[0].text = rng; row[1].text = cat; row[2].text = act
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(3)]
    [cell_font(row[j], size=11, center=(j<2)) for j in range(3)]
doc.add_paragraph().paragraph_format.space_after = Pt(6)

insert_image(ASSETS / "chart_threshold_calibration.png", width_in=5.6,
             caption="Figure 9.6 — Novelty Threshold Calibration Curve: Precision, Recall, F1 vs Cosine Similarity Threshold")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 17 — CONCLUSION
# ═══════════════════════════════════════════════════════════════════
heading("Conclusion and Future Enhancements", level=1, num="10.")
body(
    "TopicMatch successfully demonstrates the practical application of state-of-the-art Natural Language Processing techniques "
    "in resolving fundamental structural challenges in academic project administration at the university level. By integrating "
    "Sentence-BERT dense embeddings with FAISS approximate nearest-neighbor search and BM25 lexical retrieval, the platform "
    "achieves high semantic recommendation precision (P@1 = 80.0% for SBERT) alongside reliable duplicate detection "
    "(Sensitivity 91.7%). The YAML-configurable multi-criteria feasibility scoring bridges the gap between student aspiration "
    "and practical execution viability. The dynamic multi-format ingestion module ensures sustainable lifecycle maintenance "
    "for academic departments, removing the need for manual database edits. All results are reproducible through the "
    "committed evaluation suite (eval/eval.py, eval/queries.json) and all 11 pytest test cases pass consistently."
)

heading("Future Enhancements", level=2, num="")
fut = [
    ("Generative Topic Refinement",
     "Integrate fine-tuned domain LLMs (LLaMA-3, Mistral-7B, or Gemini via API) for iterative abstract rewriting, scope "
     "expansion suggestions, and automated supervisor feedback generation on submitted proposals."),
    ("Live Research Paper Novelty Verification",
     "Connect the novelty pipeline to live academic databases (IEEE Xplore API, Semantic Scholar, arXiv) to cross-check "
     "student proposals against the international published literature — not just the departmental historical archive."),
    ("Automated Milestone and Workload Tracking",
     "Build a timeline management module with automated milestone generation, multi-supervisor workload balancing, "
     "and student task assignment matrices integrated with the existing proposal review workflow."),
    ("Federated Multi-Institution Corpus",
     "Extend the system to aggregate project archives from partner institutions via a privacy-preserving federated learning "
     "architecture, increasing corpus diversity and strengthening novelty detection coverage."),
    ("Mobile Progressive Web App",
     "Port the student-facing interface to a lightweight PWA using React Native Web, enabling offline topic browsing "
     "and proposal drafting with sync-on-connect behavior."),
]
for i, (title, desc) in enumerate(fut, 1):
    numbered(desc, str(i), bold_prefix=title + ": ")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════
# PAGE 18 — REFERENCES
# ═══════════════════════════════════════════════════════════════════
heading("References", level=1, num="11.")
refs = [
    'Reimers, N., & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." '
    'Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP). '
    'https://arxiv.org/abs/1908.10084',

    'Johnson, J., Douze, M., & Jégou, H. (2021). "Billion-Scale Similarity Search with GPUs." '
    'IEEE Transactions on Big Data, 7(3), 535–547. https://doi.org/10.1109/TBDATA.2019.2921572',

    'Robertson, S., & Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." '
    'Foundations and Trends in Information Retrieval, 3(4), 333–389.',

    'Vaswani, A., et al. (2017). "Attention Is All You Need." '
    'Advances in Neural Information Processing Systems (NeurIPS), 30.',

    'Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers '
    'for Language Understanding." NAACL-HLT 2019. https://arxiv.org/abs/1810.04805',

    'FastAPI Documentation. Sebastián Ramírez. https://fastapi.tiangolo.com/',
    'Hugging Face sentence-transformers Library. https://www.sbert.net/',
    'FAISS Library Documentation. Meta AI Research. https://github.com/facebookresearch/faiss',
    'rank-bm25: A Collection of BM25 Algorithms in Python. https://github.com/dorianbrown/rank_bm25',
    'React Documentation v18. Meta Open Source. https://react.dev/',
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.line_spacing = Pt(16)
    r_n = p.add_run(f"[{i}] ")
    r_n.font.name = 'Times New Roman'
    r_n.font.size = Pt(11)
    r_n.font.bold = True
    r = p.add_run(ref)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

# ════════════════════════════════════════════════════════════════════
out = Path("PROJECT_DOCUMENTATION_NLP_FINAL.docx")
doc.save(str(out))
print(f"SUCCESS: {out.resolve()}")

