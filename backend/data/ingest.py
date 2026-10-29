"""
Dataset Ingestion & Preprocessing Pipeline
Supports: .csv, .txt, .pdf, .docx, .json
Extracts, cleans, auto-tags tech stack & domains, and normalizes into ProjectEntry schema.
"""
from __future__ import annotations

import csv
import io
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from data.schema import ProjectEntry
from data.tags import TAG_LIST

# Mapping domain keywords
DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "healthcare": ["health", "healthcare", "hospital", "patient", "medical", "doctor", "disease", "clinical", "medicine", "cancer", "diagnosis", "clinic"],
    "edtech": ["student", "school", "college", "exam", "tutor", "learning", "education", "edtech", "course", "quiz", "attendance", "teacher", "study", "classroom"],
    "finance": ["bank", "banking", "stock", "crypto", "credit", "fraud", "payment", "money", "trading", "wallet", "invoice", "fintech", "loan"],
    "smart-city": ["traffic", "parking", "vehicle", "urban", "waste", "garbage", "transport", "metro", "city", "street", "smart city"],
    "security": ["cyber", "cybersecurity", "malware", "phishing", "encryption", "auth", "security", "vulnerability", "attack", "firewall"],
    "iot": ["iot", "sensor", "arduino", "raspberry", "hardware", "drone", "embedded", "smart-home", "rfid"],
    "e-commerce": ["ecommerce", "shopping", "store", "product", "cart", "recommendation", "retail", "marketplace", "e-commerce"],
    "environment": ["environment", "wildlife", "energy", "solar", "weather", "agriculture", "crop", "plant", "forest", "green"],
    "hr-tech": ["resume", "job", "recruitment", "interview", "hiring", "applicant", "career", "hr-tech"],
    "social": ["social", "community", "ngo", "volunteer", "donation", "chat", "network"],
    "developer-tools": ["compiler", "ide", "git", "cli", "debugger", "testing", "benchmark", "code editor", "developer tools"],
}

# Mapping tech stack synonyms to canonical TAG_LIST
TECH_SYNONYMS: dict[str, list[str]] = {
    "nlp": ["bert", "llm", "gpt", "transformer", "spacy", "nltk", "chatbot", "sentiment", "text", "summarization", "translation", "huggingface"],
    "computer-vision": ["opencv", "yolo", "cnn", "image", "video", "face detection", "object detection", "camera", "segmentation", "ocr"],
    "deep-learning": ["deep learning", "neural network", "pytorch", "tensorflow", "keras", "lstm", "gan", "diffusion"],
    "machine-learning": ["machine learning", "scikit-learn", "sklearn", "xgboost", "random forest", "regression", "classification", "clustering"],
    "data-analysis": ["data analysis", "pandas", "numpy", "matplotlib", "seaborn", "analytics", "visualization", "forecasting"],
    "fastapi": ["fastapi", "rest api", "uvicorn"],
    "flask": ["flask"],
    "django": ["django"],
    "react": ["react", "reactjs", "nextjs"],
    "nodejs": ["nodejs", "node.js", "expressjs", "express"],
    "python": ["python", "python3", "py"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "docker": ["docker", "container", "docker-compose", "kubernetes"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "mongodb": ["mongodb", "nosql"],
    "firebase": ["firebase", "firestore"],
    "api-integration": ["api", "webhook", "rest", "integration", "microservice"],
}


def _clean_text(s: str) -> str:
    """Normalize whitespace and strip control characters."""
    if not s:
        return ""
    s = re.sub(r"[\r\n\t]+", " ", str(s))
    return re.sub(r"\s+", " ", s).strip()


def extract_tech_tags(text: str, existing_tags: list[str] | None = None) -> list[str]:
    """Detect canonical tech stack tags from text or normalize existing tags."""
    found: set[str] = set()
    text_lower = text.lower()

    # Check direct canonical tags in text
    for tag in TAG_LIST:
        pattern = r"\b" + re.escape(tag) + r"\b"
        if re.search(pattern, text_lower):
            found.add(tag)

    # Check synonyms using word boundaries
    for canonical_tag, syns in TECH_SYNONYMS.items():
        for syn in syns:
            if re.search(r"\b" + re.escape(syn) + r"\b", text_lower):
                found.add(canonical_tag)
                break

    # If existing tags were provided, validate and add
    if existing_tags:
        for t in existing_tags:
            t_clean = t.strip().lower()
            if t_clean in TAG_LIST:
                found.add(t_clean)
            elif t_clean in TECH_SYNONYMS:
                found.add(t_clean)
            else:
                for canonical, syns in TECH_SYNONYMS.items():
                    if t_clean in syns:
                        found.add(canonical)

    if not found:
        found.add("python")  # sensible academic default
    return sorted(found)


def extract_domain_tags(text: str, existing_domains: list[str] | None = None) -> list[str]:
    """Detect domain categories from text."""
    found: set[str] = set()
    text_lower = text.lower()

    for domain, kws in DOMAIN_KEYWORDS.items():
        for kw in kws:
            if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                found.add(domain)
                break

    if existing_domains:
        for d in existing_domains:
            d_clean = d.strip().lower()
            if d_clean:
                found.add(d_clean)

    if not found:
        found.add("web")
    return sorted(found)


def parse_csv(content: bytes) -> list[dict[str, Any]]:
    """Parse CSV content with flexible column naming."""
    text = content.decode("utf-8-sig", errors="replace")
    # Detect dialect / delimiter
    delimiter = ","
    try:
        sample = text[:2048]
        dialect = csv.Sniffer().sniff(sample)
        delimiter = dialect.delimiter
    except Exception:
        pass

    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    records = []
    current_year = datetime.now().year

    for row in reader:
        # Standardize key names (lowercase, stripped)
        clean_row = {k.strip().lower(): v.strip() for k, v in row.items() if k and v}
        if not clean_row:
            continue

        # Find title
        title = ""
        for key in ["title", "project_title", "project title", "topic", "project", "name"]:
            if key in clean_row and clean_row[key]:
                title = clean_row[key]
                break

        if not title:
            # Fallback: first non-empty value
            for v in clean_row.values():
                if len(v) > 5:
                    title = v
                    break

        if not title:
            continue

        # Find abstract
        abstract = ""
        for key in ["abstract", "description", "summary", "details", "desc", "overview"]:
            if key in clean_row and clean_row[key]:
                abstract = clean_row[key]
                break
        if not abstract:
            abstract = title

        # Tags
        tags_raw = clean_row.get("tech_stack_tags") or clean_row.get("tech_stack") or clean_row.get("skills") or clean_row.get("technologies") or ""
        tags_list = [t.strip() for t in re.split(r"[,;|]+", tags_raw) if t.strip()]

        # Domains
        dom_raw = clean_row.get("domain_tags") or clean_row.get("domain") or clean_row.get("category") or ""
        dom_list = [d.strip() for d in re.split(r"[,;|]+", dom_raw) if d.strip()]

        # Year
        try:
            year = int(clean_row.get("year", current_year))
        except Exception:
            year = current_year

        # Dept
        dept = clean_row.get("department") or clean_row.get("dept") or "Computer Science"

        records.append({
            "title": _clean_text(title),
            "abstract": _clean_text(abstract),
            "tech_stack_tags": tags_list,
            "domain_tags": dom_list,
            "year": year,
            "department": dept,
        })
    return records


def parse_txt(content: bytes) -> list[dict[str, Any]]:
    """Parse TXT files: can be JSON array, Name-Roll-Title lines, or Project blocks."""
    text = content.decode("utf-8-sig", errors="replace").strip()
    if not text:
        return []

    # Try JSON
    if text.startswith("[") or text.startswith("{"):
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                data = [data]
            records = []
            for item in data:
                if isinstance(item, dict) and "title" in item:
                    records.append({
                        "title": _clean_text(item["title"]),
                        "abstract": _clean_text(item.get("abstract", item["title"])),
                        "tech_stack_tags": item.get("tech_stack_tags", []),
                        "domain_tags": item.get("domain_tags", []),
                        "year": int(item.get("year", datetime.now().year)),
                        "department": item.get("department", "Computer Science"),
                    })
            if records:
                return records
        except Exception:
            pass

    # Line-based parsing
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    records = []
    current_year = datetime.now().year

    for line in lines:
        # Check if line is "Name, Roll, Title" format
        parts = [p.strip() for p in line.split(",") if p.strip()]
        if len(parts) >= 3 and not line.lower().startswith("name"):
            # Assume parts[2] is title
            title = ", ".join(parts[2:])
            records.append({
                "title": _clean_text(title),
                "abstract": _clean_text(title),
                "tech_stack_tags": [],
                "domain_tags": [],
                "year": current_year,
                "department": "Computer Science",
            })
        elif len(parts) == 2 and not line.lower().startswith("title"):
            records.append({
                "title": _clean_text(parts[0]),
                "abstract": _clean_text(parts[1]),
                "tech_stack_tags": [],
                "domain_tags": [],
                "year": current_year,
                "department": "Computer Science",
            })
        elif len(line) >= 8:
            # Single project title per line
            records.append({
                "title": _clean_text(line),
                "abstract": _clean_text(line),
                "tech_stack_tags": [],
                "domain_tags": [],
                "year": current_year,
                "department": "Computer Science",
            })
    return records


def parse_pdf(content: bytes) -> list[dict[str, Any]]:
    """Extract project titles and summaries from PDF."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise RuntimeError("pypdf not installed. Run: pip install pypdf")

    reader = PdfReader(io.BytesIO(content))
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"

    # Treat text as txt format or paragraph chunks
    return parse_txt(full_text.encode("utf-8"))


def parse_docx(content: bytes) -> list[dict[str, Any]]:
    """Extract projects from DOCX (tables or paragraphs)."""
    try:
        import docx
    except ImportError:
        raise RuntimeError("python-docx not installed. Run: pip install python-docx")

    doc = docx.Document(io.BytesIO(content))
    records: list[dict[str, Any]] = []
    current_year = datetime.now().year

    # Check tables first
    for table in doc.tables:
        if len(table.rows) > 1:
            headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
            title_col = -1
            desc_col = -1
            for idx, h in enumerate(headers):
                if any(k in h for k in ["title", "topic", "project", "name"]):
                    title_col = idx
                elif any(k in h for k in ["abstract", "description", "summary"]):
                    desc_col = idx

            if title_col != -1:
                for row in table.rows[1:]:
                    cells = [c.text.strip() for c in row.cells]
                    if len(cells) > title_col and cells[title_col]:
                        title = cells[title_col]
                        desc = cells[desc_col] if (desc_col != -1 and len(cells) > desc_col and cells[desc_col]) else title
                        records.append({
                            "title": _clean_text(title),
                            "abstract": _clean_text(desc),
                            "tech_stack_tags": [],
                            "domain_tags": [],
                            "year": current_year,
                            "department": "Computer Science",
                        })

    if records:
        return records

    # Paragraphs fallback
    para_text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
    return parse_txt(para_text.encode("utf-8"))


def ingest_file(filename: str, content: bytes) -> list[dict[str, Any]]:
    """Dispatch file parsing based on extension."""
    ext = Path(filename).suffix.lower()
    if ext == ".csv":
        return parse_csv(content)
    elif ext in [".txt", ".json"]:
        return parse_txt(content)
    elif ext == ".pdf":
        return parse_pdf(content)
    elif ext in [".docx", ".doc"]:
        return parse_docx(content)
    else:
        # Default try as text
        return parse_txt(content)


def preprocess_records(
    raw_records: list[dict[str, Any]],
    existing_corpus: list[ProjectEntry],
) -> tuple[list[ProjectEntry], int]:
    """Clean, auto-tag, deduplicate, and convert raw records to valid ProjectEntry objects."""
    existing_titles_norm = {
        re.sub(r"[^\w\s]", "", e.title.lower()).strip()
        for e in existing_corpus
    }

    # Find highest sequence ID for current year
    current_year = datetime.now().year
    highest_seq = 0
    for e in existing_corpus:
        m = re.match(r"(?:gls|up)-(\d{4})-(\d+)", e.id)
        if m and int(m.group(1)) == current_year:
            seq = int(m.group(2))
            if seq > highest_seq:
                highest_seq = seq

    new_entries: list[ProjectEntry] = []
    duplicate_count = 0

    for r in raw_records:
        title = r.get("title", "").strip()
        if not title or len(title) < 4:
            continue

        title_norm = re.sub(r"[^\w\s]", "", title.lower()).strip()
        if title_norm in existing_titles_norm:
            duplicate_count += 1
            continue

        existing_titles_norm.add(title_norm)
        abstract = r.get("abstract", "") or title
        full_text = f"{title}. {abstract}"

        tech_tags = extract_tech_tags(full_text, r.get("tech_stack_tags"))
        domain_tags = extract_domain_tags(full_text, r.get("domain_tags"))
        year = r.get("year") or current_year
        dept = r.get("department") or "Computer Science"

        highest_seq += 1
        entry_id = f"up-{year}-{highest_seq:03d}"

        new_entry = ProjectEntry(
            id=entry_id,
            title=title,
            abstract=abstract,
            year=year,
            department=dept,
            tech_stack_tags=tech_tags,
            domain_tags=domain_tags,
            language="en",
        )
        new_entries.append(new_entry)

    return new_entries, duplicate_count
