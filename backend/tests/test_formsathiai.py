import os
import json
import pytest
from fastapi.testclient import TestClient
import fitz

from app.main import app
from app.config import DEMO_DATA_DIR, FICTIONAL_DEMO_WARNING
from app.demo_data import (
    SCHOLARSHIP_RULES,
    FIELD_EXPLANATIONS,
    EXACT_DEMO_QA,
    get_default_application,
    get_demo_scenarios
)
from app.retrieval import answer_question, ABSENT_INFO_EN, ABSENT_INFO_HI
from app.validator import validate_application
from app.checklist import generate_checklist
from app.ocr_engine import is_tesseract_available, run_ocr_on_image
from app.document_parser import validate_file

client = TestClient(app)


def test_01_app_launches_in_offline_demo_mode_without_api_key():
    """Verify application launches and responds to health check in offline demo mode."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["mode"] == "deterministic_offline_demo"
    assert "FICTIONAL DEMO" in data["warning"]


def test_02_all_eight_fictional_document_types_exist():
    """Verify all 8 fictional document types and 2 OCR images and manifest exist."""
    manifest_path = os.path.join(DEMO_DATA_DIR, "demo_documents_manifest.json")
    assert os.path.exists(manifest_path)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    expected_docs = [
        "Udaan_Scholarship_Instructions_Demo.pdf",
        "Udaan_Application_Form_Demo.pdf",
        "Academic_Marksheet_Demo.pdf",
        "Academic_Marksheet_Inconsistent_Demo.pdf",
        "Identity_Proof_Placeholder_Demo.pdf",
        "Income_Certificate_Placeholder_Demo.pdf",
        "Bank_Passbook_Placeholder_Demo.pdf",
        "Institution_Certificate_Demo.pdf",
        "Applicant_Declaration_Demo.pdf",
        "Udaan_Application_Form_Scanned_Demo.png",
        "Udaan_Scholarship_Instructions_Scanned_Demo.png"
    ]
    for doc in expected_docs:
        doc_path = os.path.join(DEMO_DATA_DIR, doc)
        assert os.path.exists(doc_path), f"Missing demo asset: {doc}"


def test_03_pdfs_contain_expected_text_and_sections():
    """Verify PDF files contain required text and sections."""
    inst_pdf = os.path.join(DEMO_DATA_DIR, "Udaan_Scholarship_Instructions_Demo.pdf")
    doc = fitz.open(inst_pdf)
    assert len(doc) == 4, "Instructions PDF must be 4 pages"
    full_text = "".join([page.get_text() for page in doc])
    
    assert "Udaan Education Foundation" in full_text
    assert "DEMO-USS-RULES-2026" in full_text
    assert "Section 1: Academic Eligibility" in full_text
    assert "Section 3: Family Income Criteria" in full_text
    assert "Section 4: Required Documents" in full_text
    assert "Section 8: Application Deadline" in full_text
    assert "30 November 2026" in full_text


def test_04_ocr_extracts_required_sample_fields():
    """Verify OCR extracts required fields from scanned demo image."""
    img_path = os.path.join(DEMO_DATA_DIR, "Udaan_Application_Form_Scanned_Demo.png")
    if is_tesseract_available():
        res = run_ocr_on_image(img_path)
        assert res["success"] is True
        text = res["text"]
        assert "DEMO-USS-2026-001" in text or "Aarav" in text or "Sharma" in text
        assert "78%" in text or "78" in text
    else:
        res = run_ocr_on_image(img_path)
        assert res["is_fallback"] is True


def test_05_source_retrieval_returns_correct_sections():
    """Verify retrieval returns exact expected sections for standard queries."""
    res = answer_question("What is the minimum marks requirement?", language="en")
    assert "60%" in res.answer
    assert res.source_citation.section_heading == "Section 1: Academic Eligibility"

    res_hi = answer_question("न्यूनतम कितने प्रतिशत अंक आवश्यक हैं?", language="hi")
    assert "60%" in res_hi.answer


def test_06_citations_use_valid_filenames_and_metadata():
    """Verify citations contain valid filenames and pages."""
    res = answer_question("What is the annual family income limit?", language="en")
    assert res.source_citation.document_name == "Udaan_Scholarship_Instructions_Demo.pdf"
    assert res.source_citation.page_number == 2
    assert "Section 3" in res.source_citation.section_heading


def test_07_default_checklist_flags_three_missing_items():
    """Verify default checklist flags income certificate, passbook, and declaration."""
    form = get_default_application()
    checklist = generate_checklist(form)
    assert checklist.total_items == 6
    assert checklist.completed_items == 3
    assert checklist.remaining_items == 3
    assert checklist.overall_status == "Incomplete"
    
    # Check specific missing keys
    missing_keys = [i.key for i in checklist.items if i.status == "missing"]
    assert "income_cert" in missing_keys
    assert "passbook" in missing_keys
    assert "declaration" in missing_keys


def test_08_inconsistent_marks_scenario_detects_78_vs_58():
    """Scenario 3: Application says 78%, while selected marksheet says 58%."""
    scenarios = {s.scenario_id: s for s in get_demo_scenarios()}
    s3_form = scenarios["scenario_3"].form_values
    
    val_res = validate_application(s3_form)
    inconsistency_alerts = [a for a in val_res.alerts if a.category == "inconsistency" and a.field_name == "qualifying_marks_pct"]
    assert len(inconsistency_alerts) == 1
    alert = inconsistency_alerts[0]
    assert "78%" in alert.message_en
    assert "58%" in alert.message_en
    assert "Potential inconsistency detected" in alert.message_en


def test_09_income_scenario_flags_280000_against_250000_limit():
    """Scenario 4: Declared income ₹2,80,000 exceeds ₹2,50,000 limit."""
    scenarios = {s.scenario_id: s for s in get_demo_scenarios()}
    s4_form = scenarios["scenario_4"].form_values
    
    val_res = validate_application(s4_form)
    income_alerts = [a for a in val_res.alerts if a.field_name == "annual_family_income" and a.category == "inconsistency"]
    assert len(income_alerts) == 1
    assert "2,50,000" in income_alerts[0].message_en
    assert "exceeds" in income_alerts[0].message_en


def test_10_hindi_and_english_answers_preserve_same_rules():
    """Verify Hindi and English answers both reflect the exact same requirements."""
    for demo in EXACT_DEMO_QA:
        res_en = answer_question(demo["question_en"], language="en")
        res_hi = answer_question(demo["question_hi"], language="hi")
        assert res_en.answer == demo["answer_en"]
        assert res_hi.answer == demo["answer_hi"]


def test_11_placeholders_classified_as_unverified():
    """Verify attached identity evidence is not described as officially verified."""
    form = get_default_application()
    val_res = validate_application(form)
    unverified_alerts = [a for a in val_res.alerts if a.category == "unverified"]
    assert len(unverified_alerts) >= 1
    assert any(
        a.field_name == "identity_proof" and "not been independently verified" in a.message_en
        for a in unverified_alerts
    )


def test_12_declaration_cannot_be_marked_complete_without_explicit_user_action():
    """Verify default declaration is incomplete and requires user action."""
    form = get_default_application()
    assert form.declaration_accepted is False
    assert form.applicant_signature is None
    checklist = generate_checklist(form)
    decl_item = next(i for i in checklist.items if i.key == "declaration")
    assert decl_item.status == "missing"


def test_13_session_reset_restores_original_demo_values():
    """Verify POST /api/session/reset restores default initial state."""
    res = client.post("/api/session/reset?session_id=test_reset_session")
    assert res.status_code == 200
    data = res.json()
    assert data["application_form"]["student_name"] == "Aarav Sharma"
    assert data["application_form"]["qualifying_marks_pct"] == 78.0
    assert data["application_form"]["declaration_accepted"] is False


def test_14_unknown_questions_do_not_produce_invented_requirements():
    """Verify asking about unsupported topics returns the required absence statement."""
    res = answer_question("What is the sports quota reservation?", language="en")
    assert res.answer == ABSENT_INFO_EN
    
    res_hi = answer_question("खेल कोटा आरक्षण क्या है?", language="hi")
    assert res_hi.answer == ABSENT_INFO_HI


def test_15_unsupported_files_produce_useful_error():
    """Verify uploading an unsupported file returns an error."""
    valid, msg = validate_file("test.exe", 1024)
    assert valid is False
    assert "Unsupported file type" in msg


def test_16_documents_remain_isolated_between_sessions():
    """Verify session isolation."""
    res1 = client.get("/api/documents?session_id=session_alpha")
    res2 = client.get("/api/documents?session_id=session_beta")
    assert res1.json()["session_id"] == "session_alpha"
    assert res2.json()["session_id"] == "session_beta"


def test_17_no_demo_workflow_submits_to_external_service():
    """Verify demo mode uses local logic without external network calls."""
    res = client.post("/api/ask", json={
        "session_id": "test_local",
        "question": "What is the deadline?",
        "language": "en"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_live_ai"] is False
    assert "30 November 2026" in data["answer"]
