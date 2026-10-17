import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from ..demo_data import SCHOLARSHIP_RULES, FIELD_EXPLANATIONS, EXACT_DEMO_QA, get_default_application, get_demo_scenarios
from ..session_manager import session_manager
from ..config import DEMO_DATA_DIR, FICTIONAL_DEMO_WARNING

router = APIRouter(prefix="/api/demo", tags=["demo"])


class ScenarioSelectRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    scenario_id: str = Field(min_length=1, max_length=64)


@router.get("")
def get_demo_data(session_id: str = Query(..., min_length=1, max_length=128)):
    """Get full demo scholarship details, current application state, and rules."""
    session = session_manager.get_session(session_id)
    return {
        "scholarship": SCHOLARSHIP_RULES,
        "application_form": session.application_form,
        "field_explanations": FIELD_EXPLANATIONS,
        "predefined_questions": EXACT_DEMO_QA,
        "fictional_warning": FICTIONAL_DEMO_WARNING
    }


@router.get("/scenarios")
def list_scenarios():
    """List available test scenarios."""
    scenarios = get_demo_scenarios()
    return {
        "scenarios": [
            {
                "scenario_id": s.scenario_id,
                "title_en": s.title_en,
                "title_hi": s.title_hi,
                "description_en": s.description_en,
                "description_hi": s.description_hi
            } for s in scenarios
        ]
    }


@router.post("/scenario")
def select_scenario(req: ScenarioSelectRequest):
    """Load a specific demo scenario into the current session."""
    session = session_manager.get_session(req.session_id)
    scenarios = {s.scenario_id: s for s in get_demo_scenarios()}
    
    if req.scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail=f"Scenario '{req.scenario_id}' not found.")
    
    selected = scenarios[req.scenario_id]
    session.application_form = selected.form_values.model_copy()
    
    return {
        "message": f"Loaded {selected.title_en}",
        "scenario": selected,
        "application_form": session.application_form
    }


@router.get("/files/{filename}")
def download_demo_file(filename: str):
    """Serve demo PDFs, PNGs, and TXT files directly."""
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(DEMO_DATA_DIR, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    media_type = "application/pdf" if safe_filename.endswith(".pdf") else \
                 "image/png" if safe_filename.endswith(".png") else \
                 "text/plain" if safe_filename.endswith(".txt") else "application/octet-stream"
    return FileResponse(file_path, media_type=media_type, filename=safe_filename)
