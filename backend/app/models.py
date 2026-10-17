from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class ApplicationFormData(BaseModel):
    application_id: str = Field(default="DEMO-USS-2026-001", max_length=80)
    student_name: str = Field(default="Aarav Sharma", max_length=120)
    dob: str = Field(default="15/08/2007", max_length=32)
    course: str = Field(default="B.Tech Computer Science", max_length=200)
    study_year: str = Field(default="First year", max_length=80)
    institution: str = Field(default="Sunrise Institute of Technology", max_length=200)
    qualifying_marks_pct: float = Field(default=78.0, ge=0, le=100, allow_inf_nan=False)
    annual_family_income: int = Field(default=180000, ge=0, le=1_000_000_000_000)
    marksheet_attached: bool = True
    identity_proof_attached: bool = True
    income_cert_attached: bool = False
    passbook_attached: bool = False
    institution_cert_attached: bool = True
    declaration_accepted: bool = False
    applicant_signature: Optional[str] = Field(default=None, max_length=120)
    declaration_date: Optional[str] = Field(default=None, max_length=32)
    bank_account_holder: str = Field(default="Aarav Sharma", max_length=120)
    bank_account_reference: str = Field(default="DEMO-ACCOUNT-0001", max_length=80)
    application_status: str = Field(default="Incomplete", max_length=40)
    active_marksheet_filename: str = Field(default="Academic_Marksheet_Demo.pdf", max_length=255)


class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    file_type: str
    file_size_bytes: int
    page_count: int = 1
    upload_timestamp: str
    extraction_method: Literal["digital_pdf", "ocr_image", "fallback_extracted"]
    ocr_confidence: Optional[float] = None
    extracted_text: str
    needs_ocr_review: bool = False
    is_fictional_placeholder: bool = False
    verification_status: Literal["verified", "unverified", "missing"] = "unverified"


class DocumentChunk(BaseModel):
    chunk_id: str
    document_filename: str
    section_title: str
    page_number: int
    text_content: str


class AskQuestionRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=500)
    language: Literal["en", "hi"] = "en"
    use_live_llm: bool = False


class SourceCitation(BaseModel):
    document_name: str
    page_number: Optional[int] = None
    section_heading: Optional[str] = None
    supporting_quote: Optional[str] = None


class AskQuestionResponse(BaseModel):
    question: str
    language: Literal["en", "hi"]
    answer: str
    source_citation: SourceCitation
    is_live_ai: bool = False
    is_predefined_grounded: bool = True
    warning: str


class ChecklistItem(BaseModel):
    key: str
    title_en: str
    title_hi: str
    status: Literal["completed", "missing", "unverified"]
    is_placeholder: bool = False
    source_document: Optional[str] = None
    details_en: str
    details_hi: str


class ChecklistResponse(BaseModel):
    total_items: int = 6
    completed_items: int = 0
    remaining_items: int = 0
    overall_status: Literal["Complete", "Incomplete"] = "Incomplete"
    items: List[ChecklistItem]
    disclaimer: str


class ValidationAlert(BaseModel):
    category: Literal["confirmed", "missing", "inconsistency", "unverified", "unavailable"]
    field_name: str
    message_en: str
    message_hi: str
    resolution_hint_en: str
    resolution_hint_hi: str
    severity: Literal["info", "warning", "error"]


class ValidationResponse(BaseModel):
    application_id: str
    is_eligible: Optional[bool] = None
    eligibility_summary_en: str
    eligibility_summary_hi: str
    alerts: List[ValidationAlert]
    fictional_warning: str


class FieldExplanation(BaseModel):
    field_key: str
    label_en: str
    label_hi: str
    explanation_en: str
    explanation_hi: str
    source_reference: Optional[str] = None
    required_in_instructions: bool = True


class DemoScenario(BaseModel):
    scenario_id: str
    title_en: str
    title_hi: str
    description_en: str
    description_hi: str
    form_values: ApplicationFormData


class OcrCorrectionRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=80)
    session_id: str = Field(min_length=1, max_length=128)
    corrected_text: str = Field(max_length=100_000)


class ConsentRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    consent_given: bool
