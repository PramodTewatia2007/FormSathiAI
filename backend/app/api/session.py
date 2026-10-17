from fastapi import APIRouter, Query
from ..models import ConsentRequest, ApplicationFormData
from ..session_manager import session_manager

router = APIRouter(prefix="/api", tags=["session"])


@router.post("/session/consent")
def set_consent(req: ConsentRequest):
    """Set or update user consent for personal data processing."""
    session = session_manager.get_session(req.session_id)
    if not req.consent_given:
        # Withdrawing consent also removes previously uploaded documents and
        # any user-entered form data from this temporary session.
        session.reset()
        return {
            "session_id": req.session_id,
            "consent_given": False,
            "message": "Consent withdrawn and temporary session data cleared.",
            "application_form": session.application_form,
        }
    session.consent_given = req.consent_given
    return {
        "session_id": req.session_id,
        "consent_given": session.consent_given,
        "message": "User consent updated." if session.consent_given else "User consent revoked."
    }


@router.post("/session/reset")
def reset_session_endpoint(session_id: str = Query(..., min_length=1, max_length=128)):
    """Reset session state, form data, and delete all uploaded documents."""
    session = session_manager.reset_session(session_id)
    return {
        "session_id": session_id,
        "message": "Session reset successfully. All uploaded temporary files have been cleared.",
        "application_form": session.application_form,
        "consent_given": session.consent_given
    }


@router.get("/session/status")
def get_session_status(session_id: str = Query(..., min_length=1, max_length=128)):
    """Get current session status, consent state, and document count."""
    session = session_manager.get_session(session_id)
    return {
        "session_id": session_id,
        "consent_given": session.consent_given,
        "document_count": len(session.documents),
        "application_form": session.application_form
    }


@router.post("/form/update")
def update_form_data(
    form_data: ApplicationFormData,
    session_id: str = Query(..., min_length=1, max_length=128)
):
    """Update current session's application form state."""
    session = session_manager.get_session(session_id)
    session.application_form = form_data
    return {
        "message": "Application form updated.",
        "application_form": session.application_form
    }
