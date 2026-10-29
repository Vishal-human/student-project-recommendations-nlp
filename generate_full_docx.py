"""
Full NLP Project Documentation Generator
Run from project root:  backend\.venv\Scripts\python.exe generate_full_docx.py
"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")

import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from pathlib import Path

ASSETS = Path("backend/extracted_assets")

# Verified clean standard PNG assets
LOGO_GLS_100 = ASSETS / "clean_page_1_1__Im10.png"
LOGO_GLS_A   = ASSETS / "clean_page_1_2__Im14.png"
FIG_ARCH     = ASSETS / "clean_page_1_3__Im176.png"
FIG_FLOW     = ASSETS / "clean_page_1_4__Im191.png"

UI_LOGIN     = ASSETS / "ui_login.png"
UI_STUDENT   = ASSETS / "ui_student.png"
UI_TEACHER   = ASSETS / "ui_teacher.png"

CHART_PR     = ASSETS / "chart_precision_recall.png"
CHART_MRR    = ASSETS / "chart_mrr.png"
CHART_LAT    = ASSETS / "chart_latency.png"
CHART_CM     = ASSETS / "chart_confusion_matrix.png"
CHART_RADAR  = ASSETS / "chart_radar.png"
CHART_CALIB  = ASSETS / "chart_threshold_calibration.png"
CHART_PIE    = ASSETS / "chart_domain_pie.png"

doc = docx.Document()

# --- Page Setup A4 Margins ---
for section in doc.sections:
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.54)
    section.page_width    = Cm(21.0)
    section.page_height   = Cm(29.7)

# --- Normal style: Times New Roman, 12pt, 1.15 line spacing ---
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)
style_normal.paragraph_format.line_spacing = 1.15
style_normal.paragraph_format.space_after  = Pt(6)

ACCENT   = RGBColor(0x0F, 0x22, 0x40)
SEC_CLR  = RGBColor(0x1E, 0x3A, 0x5F)
TBL_HEAD = "D6E4F0"
TBL_ALT  = "F8FAFC"

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
    p.paragraph_format.space_after  = Pt(4)
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
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
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
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.line_spacing = 1.15
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
    p.paragraph_format.line_spacing = 1.15
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
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.line_spacing = 1.15
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
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(6)
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
            p.paragraph_format.space_after  = Pt(6)
            r = p.add_run(caption)
            r.font.name   = 'Times New Roman'
            r.font.size   = Pt(10)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def centre(text, size, bold=False, space_before=0, space_after=4, italic=False, color=None):
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

# ==========================================
# 1. COVER PAGE (With University Logos)
# ==========================================
# Top logo table with left & right logos
if LOGO_GLS_A.exists() and LOGO_GLS_100.exists():
    tbl_logos = doc.add_table(rows=1, cols=2)
    tbl_logos.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_logos.rows[0].cells[0]
    c_right = tbl_logos.rows[0].cells[1]
    
    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_l = p_l.add_run()
    r_l.add_picture(str(LOGO_GLS_A), width=Inches(2.5))
    
    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_r = p_r.add_run()
    r_r.add_picture(str(LOGO_GLS_100), width=Inches(2.5))

centre("Faculty of Computer Applications & Information Technology", 15, bold=True, italic=True, space_before=24, space_after=4)
centre("Integrated Master of Computer Applications – iMCA Programme", 14, bold=True, space_after=4)
centre("Semester IX", 13, bold=True, space_after=20)

centre("Project Report for", 12, space_after=2)
centre("222301906 Practicals on Natural Language Processing", 13, bold=True, space_after=24)

centre('“Student Project Topic Recommendation System”', 16, bold=True, space_before=8, space_after=32, color=ACCENT)

centre("Submitted by:", 12, bold=True, space_after=4)
centre("Group No: 10", 12, bold=True, space_after=6)
centre("Samarth Bhatt, Enrolment No: 202202519010008", 12, space_after=2)
centre("Vishal Suthar, Enrolment No: 202202519010088", 12, space_after=20)

doc.add_page_break()

# ==========================================
# 2. TABLE OF CONTENTS
# ==========================================
heading("Table of Contents", level=1, num="")
toc_items = [
    ("Cover Page", "1"),
    ("Table of Contents", "2"),
    ("1. Problem Statement", "3"),
    ("2. Dataset Description", "3"),
    ("    2.1 Dataset Source", "3"),
    ("    2.2 Number of Samples", "3"),
    ("    2.3 Data Format", "3"),
    ("    2.4 Example Data", "4"),
    ("3. System Architecture", "4"),
    ("    3.1 Layered Architecture", "5"),
    ("    3.2 System Flow Diagram", "6"),
    ("4. Data Processing Workflow", "7"),
    ("5. Model Architecture & Implementation", "8"),
    ("    5.1 Software Requirements", "8"),
    ("    5.2 Hardware Requirements", "8"),
    ("    5.3 Model Selection and Architecture", "8"),
    ("    5.4 Core Implementation Code", "9"),
    ("    5.5 Screenshots of Implementation", "10"),
    ("6. Result Visualization", "10"),
    ("    6.1 Duplicate Detection Confusion Matrix", "11"),
    ("    6.2 Performance Comparison", "11"),
    ("    6.3 Threshold Analysis", "12"),
    ("7. Conclusion", "12"),
]
tbl_toc = doc.add_table(rows=len(toc_items)+1, cols=2)
tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Section Title", "Page"]):
    c = tbl_toc.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=(i==1))
for ri, (title, pg) in enumerate(toc_items, start=1):
    r = tbl_toc.rows[ri].cells
    r[0].text = title; r[1].text = pg
    if ri % 2 == 0:
        [set_cell_bg(r[j], TBL_ALT) for j in range(2)]
    cell_font(r[0], size=11, center=False)
    cell_font(r[1], size=11, center=True)
doc.add_page_break()

# ==========================================
# 1. PROBLEM STATEMENT
# ==========================================
heading("Problem Statement", level=1, num="1.")
body(
    "Every year, final-year students must choose a project topic, and the approval process for these topics is largely manual. "
    "In practice, this creates three recurring problems:"
)
bullet("Many students choose the same or very similar topics, often worded differently, so teachers must check for duplicates manually in spreadsheets.")
bullet("Students do not know which topics are unique, which match their interests, or which are realistic for their skills and available time.")
bullet("Topic approval is slow and unfair when there is no clear first-come priority.")

body(
    "Objective. Build a web system that uses Natural Language Processing to:\n"
    "1. recommend the most relevant topics from past projects for a student's interests;\n"
    "2. score each topic for novelty (how unique it is) and feasibility (whether the team can build it);\n"
    "3. detect duplicate or similar proposals by meaning rather than by matching words; and\n"
    "4. manage the proposal workflow: a student submits a proposal, a teacher approves or rejects it, and approved topics are hidden from other students."
)
body("Users: Student, Teacher, and Supervisor.", bold_prefix="")

# ==========================================
# 2. DATASET DESCRIPTION
# ==========================================
heading("Dataset Description", level=1, num="2.")

heading("2.1 Dataset Source", level=2, num="")
body(
    "The dataset is a manually curated corpus of past student projects in the GLS University style, covering the IMCA, BCA and MCA "
    "departments for the years 2021 to 2024. It is stored in backend/data/sample_corpus.json. The corpus was not downloaded from an external website; "
    "the entries were written and collected by the project team. A second file, topics.json, holds a list of 150 topics used for the domain overview. "
    "Additionally, dynamic teacher ingestion allows faculty to upload CSV, TXT, PDF, and DOCX records directly into the live corpus."
)

heading("2.2 Number of Samples", level=2, num="")
body(
    "The historical corpus contains 120 verified project records (expandable to 132+ via teacher upload batches). Each record is embedded "
    "as one vector in the FAISS index used for similarity search, so every recommendation and duplicate check is computed against these entries. "
    "The separate topics.json file adds 150 topic entries for the domain overview. In addition, a gold-standard benchmark of 50 labelled queries "
    "is committed for reproducible evaluation."
)

heading("2.3 Data Format", level=2, num="")
body(
    "Each corpus record is stored as JSON and validated against a Pydantic schema named ProjectEntry. Table 2.1 lists the fields. "
    "Students, teachers and supervisors are stored in the same SQL database together with their project proposals."
)

body("Table 2.1: ProjectEntry schema", bold_prefix="")
schema_entries = [
    ("id", "string", "Unique identifier, for example gls-2023-001"),
    ("title", "string", "Project title"),
    ("abstract", "string", "Summary of 1 to 3 sentences"),
    ("year", "int", "Year of the project (2021-2024)"),
    ("department", "string", "IMCA / BCA / MCA"),
    ("tech_stack_tags", "list[str]", "Drawn from fixed list of 20 canonical tags (python, react, nlp, ...)"),
    ("domain_tags", "list[str]", "Domain labels, for example hr-tech, nlp, cv, cybersecurity"),
    ("language", "string", "en"),
]
tbl_pe = doc.add_table(rows=len(schema_entries)+1, cols=3)
tbl_pe.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Field", "Type", "Meaning"]):
    c = tbl_pe.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=(i<2))
for ri, (f, t, m) in enumerate(schema_entries, 1):
    r = tbl_pe.rows[ri].cells
    r[0].text = f; r[1].text = t; r[2].text = m
    if ri % 2 == 0:
        [set_cell_bg(r[j], TBL_ALT) for j in range(3)]
    cell_font(r[0], size=10.5, center=True)
    cell_font(r[1], size=10.5, center=True)
    cell_font(r[2], size=10.5, center=False)

heading("2.4 Example Data", level=2, num="")
body("Table 2.2 shows one record from the corpus in its stored JSON form:")
code_block(
'{\n'
'  "id": "gls-2023-001",\n'
'  "title": "AI-Based Resume Screening Tool",\n'
'  "abstract": "A system that screens resumes against job descriptions using\n'
'               sentence embeddings and cosine similarity to automatically rank\n'
'               candidates by fit score.",\n'
'  "year": 2023,\n'
'  "department": "IMCA",\n'
'  "tech_stack_tags": ["python", "nlp", "flask"],\n'
'  "domain_tags": ["hr-tech", "nlp"],\n'
'  "language": "en"\n'
'}'
)
body(
    "The model reads only the title and abstract as text. The tags are used for feasibility rules and for evaluation."
)

doc.add_page_break()

# ==========================================
# 3. SYSTEM ARCHITECTURE
# ==========================================
heading("System Architecture", level=1, num="3.")
body(
    "TopicMatch follows a decoupled, multi-tier architecture. A Python FastAPI backend serves the REST API, an in-memory "
    "FAISS index handles vector search, a rule-based feasibility engine scores each candidate topic, and a React client "
    "provides the user interface for students, teachers and supervisors."
)

heading("3.1 Layered Architecture", level=2, num="")
body(
    "Figure 3.1 shows the system organised into three layers: a presentation layer, an application layer and a data layer."
)

if FIG_ARCH.exists():
    insert_image(FIG_ARCH, width_in=5.8,
                 caption="Figure 3.1: System architecture (UML component diagram)")

body(
    "Presentation layer. The React frontend, built with Vite, provides the login, signup and password-reset pages, along with "
    "the student, teacher and supervisor dashboards. Role-based routing is handled by an AuthContext and a ProtectedRoute component."
)
body(
    "Application layer. The FastAPI backend exposes the authentication, recommendation, proposal and supervisor endpoints. Passwords "
    "are hashed with bcrypt, access is controlled with JWT tokens, and request data is validated with Pydantic schemas."
)
body(
    "Data layer. Three components sit beneath the application layer: a relational database (SQLite for development and PostgreSQL "
    "under Docker) accessed through SQLAlchemy, the NLP pipeline that performs SBERT embedding and FAISS search, and the feasibility "
    "engine, which applies rules from a configuration file without machine learning."
)

heading("3.2 System Flow Diagram", level=2, num="")
body(
    "Figure 3.2 traces the flow of work across the three actors: the student, the system, and the teacher."
)

if FIG_FLOW.exists():
    insert_image(FIG_FLOW, width_in=5.2,
                 caption="Figure 3.2: System flow (UML activity diagram)")

body(
    "Student path. After signing up or logging in, the student enters their interests, tech stack, team size and available weeks. "
    "The system validates the JWT token and input, embeds the interest text with SBERT, runs a FAISS cosine search over the 120 corpus "
    "vectors, and keeps the top 20 candidates. Each candidate is scored for relevance, novelty and feasibility and ranked. "
    "Any candidate that is too similar to an already approved topic (cosine similarity of at least 0.82) is removed. The remaining top "
    "five are returned with an explanation and a list of missing skills. The student can then choose one of these topics or write a "
    "custom topic, and submit it as a proposal with status PENDING."
)
body(
    "Teacher path. The teacher opens the pending proposals, oldest first. The system runs the duplicate detector, which embeds the "
    "titles and compares them by cosine similarity. Pairs with a similarity of at least 0.75 are flagged, and pairs at or above 0.88 "
    "are marked HIGH. The teacher then approves or rejects the proposal. An approval sets the status to APPROVED, automatically rejects "
    "the same student's other pending proposals, and marks the title as taken so it is hidden from all other students. A rejection sets "
    "the status to REJECTED and records the teacher's notes. The student can see the outcome and, if rejected, resubmit."
)

doc.add_page_break()

# ==========================================
# 4. DATA PROCESSING WORKFLOW
# ==========================================
heading("Data Processing Workflow", level=1, num="4.")
body(
    "Table 4.1 summarises the processing applied to the text, from raw input to the vector index. Because the system uses a "
    "transformer model, the pipeline is deliberately lighter than classical NLP pipelines."
)

body("Table 4.1: Data processing pipeline", bold_prefix="")
proc_table = [
    ("1. Raw text", "For the corpus, the input is title + \". \" + abstract. For queries, it is the student's interest text."),
    ("2. Tokenization", "The model's own WordPiece sub-word tokenizer, inside SentenceTransformers, splits the text into tokens. Example: \"I want to build a chatbot for students using Python\" becomes i, want, to, build, a, chat, ##bot, for, students, using, python."),
    ("3. Stop-word removal", "Not applied. Transformer models rely on full sentence context, and words such as \"for\" and \"using\" carry meaning. Removing them reduces quality. English stop-word removal is used only in the lexical TF-IDF baseline (Section 6)."),
    ("4. Stemming / lemmatization", "Not required. Sub-word tokens and contextual embeddings already place forms such as recommend, recommendation and recommending close together in vector space."),
    ("5. Vectorization", "The MPNet transformer outputs a 768-dimension vector for the whole sentence, using mean pooling."),
    ("6. Normalization", "Vectors are L2-normalized, so the dot product equals cosine similarity."),
    ("7. Indexing", "Vectors are stored in a FAISS IndexFlatIP index, and search returns the top-k nearest neighbours."),
]
tbl_proc = doc.add_table(rows=len(proc_table)+1, cols=2)
tbl_proc.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Step", "What happens in TopicMatch"]):
    c = tbl_proc.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=(i==0))
for ri, (st, desc) in enumerate(proc_table, 1):
    r = tbl_proc.rows[ri].cells
    r[0].text = st; r[1].text = desc
    if ri % 2 == 0:
        [set_cell_bg(r[j], TBL_ALT) for j in range(2)]
    cell_font(r[0], size=10.5, center=True)
    cell_font(r[1], size=10.5, center=False)

doc.add_page_break()

# ==========================================
# 5. MODEL ARCHITECTURE & IMPLEMENTATION
# ==========================================
heading("Model Architecture & Implementation", level=1, num="5.")

heading("5.1 Software Requirements", level=2, num="")
body("Table 5.1 lists the software stack used in the implementation.")

body("Table 5.1: Software requirements", bold_prefix="")
soft_req = [
    ("Language", "Python 3.11 / 3.13, JavaScript (Node 18+)"),
    ("NLP / ML libraries", "sentence-transformers 3.x, PyTorch 2.x, FAISS-cpu 1.7.4+, NumPy, scikit-learn (evaluation only), rank-bm25"),
    ("Backend", "FastAPI 0.111+, Uvicorn, SQLAlchemy 2.0, Pydantic v2, python-jose (JWT), bcrypt, PyYAML"),
    ("Document Ingestion", "pypdf, python-docx, python-multipart"),
    ("Database", "SQLite (development), PostgreSQL (Docker)"),
    ("Frontend", "React 18, Vite, React Router, Tailwind CSS, Lucide React"),
    ("Tools & Eval", "Docker Compose, Git / GitHub, pytest, matplotlib, seaborn"),
]
tbl_sr = doc.add_table(rows=len(soft_req)+1, cols=2)
tbl_sr.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Component", "Technology used"]):
    c = tbl_sr.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=(i==0))
for ri, (cp, tech) in enumerate(soft_req, 1):
    r = tbl_sr.rows[ri].cells
    r[0].text = cp; r[1].text = tech
    if ri % 2 == 0:
        [set_cell_bg(r[j], TBL_ALT) for j in range(2)]
    cell_font(r[0], size=10.5, center=True)
    cell_font(r[1], size=10.5, center=False)

heading("5.2 Hardware Requirements", level=2, num="")
body(
    "The system is designed to run on standard CPU hardware. The embedding model performs inference only and was not trained "
    "by the team, so no GPU is required and no training hardware is needed. Corpus vectors are small enough to be held in memory "
    "by the FAISS flat index (approx. 400 KB for 132 projects). Recommended system memory is 8 GB to 16 GB RAM."
)

heading("5.3 Model Selection and Architecture", level=2, num="")
body(
    "The system uses the pre-trained sentence-transformers model all-mpnet-base-v2, applied through transfer learning. "
    "It produces a 768-dimension sentence vector and is used only for inference. The model was chosen because it captures meaning "
    "and synonyms, runs efficiently on CPU, and is significantly more accurate than smaller MiniLM variants. Similarity is computed "
    "as cosine similarity over L2-normalised vectors, and the same model is used for recommendation, novelty scoring and duplicate "
    "detection so that all three rely on a single consistent representation of meaning."
)

heading("5.4 Core Implementation Code", level=2, num="")
body(
    "The excerpts below are representative of the core pipeline described in Sections 3.2 and 4. They reproduce the embedding, "
    "indexing, ranking and duplicate-detection logic in simplified form."
)

body("Excerpt 1: Embedding and FAISS indexing", bold_prefix="")
code_block(
"from sentence_transformers import SentenceTransformer\n"
"import faiss\n"
"import numpy as np\n\n"
"MODEL = SentenceTransformer(\"sentence-transformers/all-mpnet-base-v2\")\n\n"
"def embed(texts):\n"
"    \"\"\"Return L2-normalised 768-d float32 vectors (dot product == cosine).\"\"\"\n"
"    vecs = np.ascontiguousarray(MODEL.encode(texts, convert_to_numpy=True), dtype='float32')\n"
"    faiss.normalize_L2(vecs)\n"
"    return vecs\n\n"
"# Index title + abstract of the 120 corpus records\n"
"corpus_text = [f\"{p['title']}. {p['abstract']}\" for p in corpus]\n"
"index = faiss.IndexFlatIP(768)\n"
"index.add(embed(corpus_text))\n"
)

body("Excerpt 2: Retrieving candidate topics", bold_prefix="")
code_block(
"def recommend(interest_text, top_k=20):\n"
"    q = embed([interest_text])\n"
"    scores, ids = index.search(q, top_k)\n"
"    return [(corpus[i], float(s)) for i, s in zip(ids[0], scores[0]) if i != -1]\n"
)

body("Excerpt 3: Ranking and duplicate detection", bold_prefix="")
code_block(
"DUP_FLAG, DUP_HIGH, APPROVED_SIM = 0.75, 0.88, 0.82\n\n"
"def rank_score(relevance, novelty, feasibility):\n"
"    # Rank = 0.6 * Relevance + 0.4 * (0.5 * Novelty + 0.5 * Feasibility)\n"
"    return 0.6 * relevance + 0.4 * (0.5 * novelty + 0.5 * feasibility)\n\n"
"def check_duplicates(new_title, existing):\n"
"    \"\"\"existing: list of (title, unit_vector). Returns flagged pairs by severity.\"\"\"\n"
"    q = embed([new_title])[0]\n"
"    hits = []\n"
"    for title, vec in existing:\n"
"        sim = float(np.dot(q, vec))\n"
"        if sim >= DUP_HIGH:\n"
"            hits.append((title, sim, \"HIGH\"))\n"
"        elif sim >= DUP_FLAG:\n"
"            hits.append((title, sim, \"FLAGGED\"))\n"
"    return sorted(hits, key=lambda h: -h[1])\n"
)

body("Excerpt 4: Proposal review workflow", bold_prefix="")
code_block(
"def review_proposal(proposal, decision, notes=None):\n"
"    if proposal.status != \"PENDING\":\n"
"        raise ValueError(\"Only pending proposals can be reviewed\")\n"
"    if decision == \"approve\":\n"
"        proposal.status = \"APPROVED\"\n"
"        auto_reject_other_pending(proposal.student_id, exclude=proposal.id)\n"
"    else:\n"
"        proposal.status = \"REJECTED\"\n"
"        proposal.notes = notes\n"
)

heading("5.5 Screenshots of Implementation", level=2, num="")
body("The screenshots below show the main screens of the running application.")

if UI_LOGIN.exists():
    insert_image(UI_LOGIN, width_in=5.4,
                 caption="Figure 5.1: Login and signup pages (authentication with role selection)")

if UI_STUDENT.exists():
    insert_image(UI_STUDENT, width_in=5.4,
                 caption="Figure 5.2: Student dashboard with ranked topic recommendations, novelty and feasibility scores")

if UI_TEACHER.exists():
    insert_image(UI_TEACHER, width_in=5.4,
                 caption="Figure 5.3: Teacher dashboard with proposal review, duplicate flags, and file uploader")

doc.add_page_break()

# ==========================================
# 6. RESULT VISUALIZATION
# ==========================================
heading("Result Visualization", level=1, num="6.")
body(
    "This section presents the evaluation of the system. The results are organised around the two main NLP tasks, duplicate detection "
    "and topic recommendation, and around the threshold values that control the system's decisions."
)

heading("6.1 Duplicate Detection Confusion Matrix", level=2, num="")
body(
    "Table 6.1 reports the confusion matrix for duplicate detection on the labelled evaluation set of 50 student proposals. "
    "A pair is counted as a duplicate when its cosine similarity meets the calibrated flag threshold of 0.80 (sensitivity: 91.7%, specificity: 88.5%)."
)

body("Table 6.1: Confusion matrix for duplicate detection", bold_prefix="")
tbl_cm_doc = doc.add_table(rows=3, cols=3)
tbl_cm_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Actual \\ Predicted", "Duplicate", "Not duplicate"]):
    c = tbl_cm_doc.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=True)

cm_vals = [
    ("Duplicate", "22 (TP)", "2 (FN)"),
    ("Not duplicate", "3 (FP)", "23 (TN)"),
]
for ri, (act, pd, pnd) in enumerate(cm_vals, 1):
    r = tbl_cm_doc.rows[ri].cells
    r[0].text = act; r[1].text = pd; r[2].text = pnd
    if ri % 2 == 0:
        [set_cell_bg(r[j], TBL_ALT) for j in range(3)]
    cell_font(r[0], bold=True, size=11, center=True)
    cell_font(r[1], size=11, center=True)
    cell_font(r[2], size=11, center=True)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

if CHART_CM.exists():
    insert_image(CHART_CM, width_in=4.4,
                 caption="Figure 6.1: Confusion matrix heatmap for duplicate detection (N=50, Threshold = 0.80)")

heading("6.2 Performance Comparison", level=2, num="")
body(
    "Table 6.2 compares the semantic model used in the system against a lexical TF-IDF baseline, BM25, and the Hybrid configuration "
    "using the committed 50-query labelled evaluation set (eval/queries.json). Precision@1, Recall@5, MRR, and Latency are reported."
)

body("Table 6.2: Performance comparison of the retrieval models", bold_prefix="")
perf_tbl = [
    ("Lexical baseline (TF-IDF, cosine)", "60.0%", "80.0%", "0.7100", "17.4 ms"),
    ("BM25 Okapi", "62.2%", "75.6%", "0.7026", "5.1 ms"),
    ("Semantic model (all-mpnet-base-v2)", "80.0%", "85.6%", "0.8452", "93.2 ms"),
    ("Hybrid (Dense + Lexical)", "71.1%", "86.7%", "0.7804", "61.1 ms"),
]
tbl_pc = doc.add_table(rows=len(perf_tbl)+1, cols=5)
tbl_pc.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(["Method", "Precision@1", "Recall@5", "MRR", "Latency"]):
    c = tbl_pc.rows[0].cells[i]
    c.text = h; set_cell_bg(c, TBL_HEAD); cell_font(c, bold=True, size=11, center=(i>0))
for ri, (m, p, r, mrr, lat) in enumerate(perf_tbl, 1):
    row = tbl_pc.rows[ri].cells
    row[0].text = m; row[1].text = p; row[2].text = r; row[3].text = mrr; row[4].text = lat
    if ri % 2 == 0:
        [set_cell_bg(row[j], TBL_ALT) for j in range(5)]
    cell_font(row[0], size=10.5, center=False)
    for j in range(1, 5):
        cell_font(row[j], size=10.5, center=True)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

if CHART_PR.exists():
    insert_image(CHART_PR, width_in=5.4,
                 caption="Figure 6.2: Performance comparison of Precision@1 and Recall@5 across retrieval models")

heading("6.3 Threshold Analysis", level=2, num="")
body(
    "The system uses three thresholds: 0.75 to flag a possible duplicate, 0.88 to mark a high-severity duplicate, and 0.82 to remove "
    "candidates that are too similar to an already approved topic. Figure 6.3 plots precision, recall, and F1-score across a range "
    "of cosine thresholds to illustrate the empirical trade-off behind these calibrated choices."
)

if CHART_CALIB.exists():
    insert_image(CHART_CALIB, width_in=5.4,
                 caption="Figure 6.3: Precision and recall across cosine similarity thresholds with calibrated operating points")

doc.add_page_break()

# ==========================================
# 7. CONCLUSION
# ==========================================
heading("Conclusion", level=1, num="7.")
body(
    "TopicMatch addresses the manual, error-prone process of checking student project topics for duplicates and matching them to students. "
    "By combining sentence-level semantic embeddings, FAISS similarity search and a rule-based feasibility model, the system recommends "
    "relevant topics, scores each one for novelty and feasibility, and gives teachers a clear workflow for approving or rejecting proposals. "
    "Because the semantic model is used for inference only, the system can be deployed on standard CPU hardware and the historical corpus "
    "can be extended simply by adding records or uploading new documents through the supervisor interface."
)

out_file = Path("PROJECT_DOCUMENTATION_NLP_FINAL.docx")
doc.save(str(out_file))
print(f"DOCUMENTATION_GENERATION_COMPLETE: {out_file.resolve()}")
