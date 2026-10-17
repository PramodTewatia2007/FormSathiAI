from typing import Optional
from fastapi import APIRouter, Query
from ..models import ApplicationFormData, ValidationResponse, ChecklistResponse
from ..validator import validate_application
from ..checklist import generate_checklist
from ..demo_data import FIELD_EXPLANATIONS
from ..session_manager import session_manager

router = APIRouter(prefix="/api", tags=["validation"])


@router.post("/validate", response_model=ValidationResponse)
def validate_endpoint(
    form_data: Optional[ApplicationFormData] = None,
    session_id: str = Query(..., min_length=1, max_length=128)
):
    """
    Validate application against scholarship rules and attached documents.
    Detects missing fields, discrepancies (e.g. 78% vs 58%), and income limits.
    """
    if form_data is None:
        session = session_manager.get_session(session_id)
        form_data = session.application_form
    return validate_application(form_data)


@router.post("/checklist", response_model=ChecklistResponse)
def checklist_endpoint(
    form_data: Optional[ApplicationFormData] = None,
    session_id: str = Query(..., min_length=1, max_length=128)
):
    """
    Calculate dynamic checklist progress.
    Tracks completed items, missing items, unverified placeholders, and declaration status.
    """
    if form_data is None:
        session = session_manager.get_session(session_id)
        form_data = session.application_form
    return generate_checklist(form_data)


@router.get("/explanations")
def get_field_explanations():
    """Retrieve bilingual explanations for form fields and required documents."""
    return FIELD_EXPLANATIONS
