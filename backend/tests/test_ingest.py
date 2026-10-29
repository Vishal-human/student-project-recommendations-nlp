"""
Tests for Data File Ingestion & Preprocessing Pipeline
Covers CSV, TXT, PDF, DOCX parsing, auto-tagging, schema validation, and deduplication.
"""
from pathlib import Path
from data.ingest import (
    parse_csv, parse_txt, preprocess_records,
    extract_tech_tags, extract_domain_tags
)
from data.schema import ProjectEntry


def test_extract_tech_tags():
    text = "Building an object detection model with PyTorch and OpenCV for traffic cameras."
    tags = extract_tech_tags(text)
    assert "computer-vision" in tags
    assert "deep-learning" in tags


def test_extract_domain_tags():
    text = "AI assistant for patient clinical diagnosis and hospital records."
    domains = extract_domain_tags(text)
    assert "healthcare" in domains


def test_parse_csv_content():
    csv_bytes = (
        b"title,description,technologies,domain,year\n"
        b"Smart Crop Irrigation,Automated soil moisture monitoring with IoT and sensors,python;iot,environment,2024\n"
    )
    records = parse_csv(csv_bytes)
    assert len(records) == 1
    assert records[0]["title"] == "Smart Crop Irrigation"
    assert "environment" in records[0]["domain_tags"]
    assert records[0]["year"] == 2024


def test_parse_txt_name_roll_title():
    txt_bytes = (
        b"Rahul Sharma, 21IMCA015, Cyber Threat Intelligence Platform Using Graph Neural Networks\n"
        b"Sneha Varma, 21IMCA092, Automated Resume Screening and ATS Matcher\n"
    )
    records = parse_txt(txt_bytes)
    assert len(records) == 2
    assert "Cyber Threat Intelligence" in records[0]["title"]
    assert "Automated Resume Screening" in records[1]["title"]


def test_preprocess_deduplication():
    existing = [
        ProjectEntry(
            id="gls-2023-001",
            title="Face Recognition Attendance System",
            abstract="Attendance system using OpenCV.",
            year=2023,
            department="IMCA",
            tech_stack_tags=["python", "computer-vision"],
            domain_tags=["edtech"],
            language="en",
        )
    ]
    raw = [
        {"title": "Face Recognition Attendance System", "abstract": "Duplicate submission"},
        {"title": "Autonomous Drone Fleet Coordination", "abstract": "Swarm robotics with ROS"},
    ]
    new_entries, duplicates = preprocess_records(raw, existing)
    assert duplicates == 1
    assert len(new_entries) == 1
    assert new_entries[0].title == "Autonomous Drone Fleet Coordination"
    assert new_entries[0].id.startswith("up-")

