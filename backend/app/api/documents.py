import logging
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from ..models import DocumentMetadata, OcrCorrectionRequest
from ..session_manager import session_manager
from ..document_parser import validate_file, parse_document
from ..config import MAX_FILE_SIZE_BYTES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])


def attachment_updates(filename: str) -> dict[str, object]:
    name = filename.lower()
    updates: dict[str, object] = {}
    if "income" in name:
        updates["income_cert_attached"] = True
    elif "passbook" in name or "bank" in name:
        updates["passbook_attached"] = True
    elif "marksheet" in name:
        updates["marksheet_attached"] = True
        updates["active_marksheet_filename"] = filename
    elif "institution" in name or "enroll" in name:
        updates["institution_cert_attached"] = True
    elif "identity" in name:
        updates["identity_proof_attached"] = True
    return updates


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = Form(..., min_length=1, max_length=128)
):
    """Upload and process a document (PDF, PNG, JPG, JPEG)."""
    session = session_manager.get_session(session_id)
    
    # Check consent
    if not session.consent_given:
        raise HTTPException(
            status_code=403,
            detail="User consent is required before processing uploaded documents containing personal or academic data."
        )

    # Validate the extension before reading, then cap the read to avoid an
    # unbounded allocation for oversized uploads.
    original_name = (file.filename or "").replace("\\", "/")
    filename = Path(original_name).name
    is_valid, err_msg = validate_file(filename, 0)
    if not is_valid:
        raise HTTPException(status_code=400, detail=err_msg)
    if any(doc.filename == filename for doc in session.documents.values()):
        raise HTTPException(status_code=409, detail="A document with this filename is already in the session.")

    contents = await file.read(MAX_FILE_SIZE_BYTES + 1)
    file_size = len(contents)
    is_valid, err_msg = validate_file(filename, file_size)
    if not is_valid:
        raise HTTPException(status_code=413, detail=err_msg)

    # Store under an opaque generated name so user supplied names cannot
    # overwrite another upload or escape the session directory.
    stored_name = f"{uuid.uuid4().hex}{Path(filename).suffix.lower()}"
    target_path = session.session_dir / stored_name
    target_path.write_bytes(contents)

    # Parse document
    try:
        metadata, chunks = parse_document(str(target_path), filename)
    except Exception:
        target_path.unlink(missing_ok=True)
        logger.exception("Document parsing failed for uploaded file")
        raise HTTPException(status_code=400, detail="The uploaded file could not be parsed. Check that it is a valid PDF or image.")

    # Store in session
    session.documents[metadata.document_id] = metadata
    session.document_paths[metadata.document_id] = str(target_path)
    session.chunks.extend(chunks)

    # Map recognizable document names to the checklist and retain the previous
    # values so deleting the upload can undo this automatic update.
    updates = attachment_updates(filename)
    session.document_attachments[metadata.document_id] = list(updates)
    for field, value in updates.items():
        if field not in session.attachment_baselines:
            session.attachment_baselines[field] = getattr(session.application_form, field)
        session.attachment_sources.setdefault(field, []).append((metadata.document_id, value))
        setattr(session.application_form, field, value)

    return {
        "message": f"Successfully uploaded and processed '{file.filename}'.",
        "document": metadata,
        "chunks_extracted": len(chunks)
    }


@router.get("")
def list_session_documents(session_id: str = Query(..., min_length=1, max_length=128)):
    """List all documents processed in the current session."""
    session = session_manager.get_session(session_id)
    return {
        "session_id": session_id,
        "count": len(session.documents),
        "documents": list(session.documents.values())
    }


@router.delete("/{document_id}")
def delete_document(document_id: str, session_id: str = Query(..., min_length=1, max_length=128)):
    """Delete a document and its temporary files from the session."""
    session = session_manager.get_session(session_id)
    if document_id not in session.documents:
        raise HTTPException(status_code=404, detail="Document not found in session.")
    
    doc = session.documents.pop(document_id)
    # Remove file from disk
    file_path = session.document_paths.pop(document_id, None)
    if file_path:
        Path(file_path).unlink(missing_ok=True)

    # Filter out chunks
    session.chunks = [c for c in session.chunks if c.document_filename != doc.filename]

    for field in session.document_attachments.pop(document_id, []):
        sources = session.attachment_sources.get(field, [])
        sources = [source for source in sources if source[0] != document_id]
        if sources:
            session.attachment_sources[field] = sources
            setattr(session.application_form, field, sources[-1][1])
        else:
            session.attachment_sources.pop(field, None)
            baseline = session.attachment_baselines.pop(field, None)
            if baseline is not None:
                setattr(session.application_form, field, baseline)

    return {
        "message": f"Document '{doc.filename}' deleted successfully.",
        "application_form": session.application_form,
    }


@router.post("/ocr-correct")
def correct_ocr_text(req: OcrCorrectionRequest):
    """Let user review and correct OCR text."""
    session = session_manager.get_session(req.session_id)
    if req.document_id not in session.documents:
        raise HTTPException(status_code=404, detail="Document not found.")

    doc = session.documents[req.document_id]
    doc.extracted_text = req.corrected_text
    doc.needs_ocr_review = False
    
    # Update corresponding chunk
    for c in session.chunks:
        if c.document_filename == doc.filename:
            c.text_content = req.corrected_text

    return {
        "message": "OCR text updated successfully.",
        "document": doc
    }
