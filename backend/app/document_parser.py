import os
import uuid
import datetime
import logging
from typing import List, Tuple
import pymupdf  # modern PyMuPDF import
from .models import DocumentMetadata, DocumentChunk
from .config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, MAX_PDF_PAGES, MAX_IMAGE_PIXELS
from .ocr_engine import run_ocr_on_image

logger = logging.getLogger(__name__)


def validate_file(file_name: str, file_size: int) -> Tuple[bool, str]:
    """Validate file extension and file size."""
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type '{ext}'. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}"
    if file_size > MAX_FILE_SIZE_BYTES:
        return False, f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB."
    return True, ""


def parse_pdf_document(file_path: str, filename: str) -> Tuple[DocumentMetadata, List[DocumentChunk]]:
    """Parse text and chunks from a digital PDF using PyMuPDF."""
    full_text_parts = []
    chunks: List[DocumentChunk] = []

    doc_id = str(uuid.uuid4())
    upload_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with pymupdf.open(file_path) as doc:
        page_count = len(doc)
        if page_count == 0 or page_count > MAX_PDF_PAGES:
            raise ValueError(f"PDF must contain between 1 and {MAX_PDF_PAGES} pages.")

        for page_idx in range(page_count):
            page_num = page_idx + 1
            page = doc.load_page(page_idx)
            text = page.get_text("text").strip()
            full_text_parts.append(f"--- Page {page_num} ---\n{text}")

            # Split into logical sections if headings exist.
            lines = text.split("\n")
            current_section = f"Page {page_num} Content"
            current_section_lines = []

            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                if line_str.startswith("Section "):
                    if current_section_lines:
                        chunks.append(DocumentChunk(
                            chunk_id=str(uuid.uuid4()),
                            document_filename=filename,
                            section_title=current_section,
                            page_number=page_num,
                            text_content="\n".join(current_section_lines)
                        ))
                        current_section_lines = []
                    current_section = line_str
                current_section_lines.append(line_str)

            if current_section_lines:
                chunks.append(DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    document_filename=filename,
                    section_title=current_section,
                    page_number=page_num,
                    text_content="\n".join(current_section_lines)
                ))

    file_size = os.path.getsize(file_path)
    is_placeholder = "placeholder" in filename.lower() or "demo" in filename.lower()
    
    meta = DocumentMetadata(
        document_id=doc_id,
        filename=filename,
        file_type="application/pdf",
        file_size_bytes=file_size,
        page_count=page_count,
        upload_timestamp=upload_time,
        extraction_method="digital_pdf",
        ocr_confidence=100.0,
        extracted_text="\n\n".join(full_text_parts),
        needs_ocr_review=False,
        is_fictional_placeholder=is_placeholder,
        verification_status="unverified"
    )
    return meta, chunks


def parse_image_document(file_path: str, filename: str) -> Tuple[DocumentMetadata, List[DocumentChunk]]:
    """Parse text and chunks from an image document using OCR engine."""
    doc_id = str(uuid.uuid4())
    upload_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    file_size = os.path.getsize(file_path)

    ocr_res = run_ocr_on_image(file_path)
    extracted_text = ocr_res.get("text", "")
    confidence = ocr_res.get("confidence", 0.0)
    is_fallback = ocr_res.get("is_fallback", False)
    
    chunks = [
        DocumentChunk(
            chunk_id=str(uuid.uuid4()),
            document_filename=filename,
            section_title="Scanned OCR Text",
            page_number=1,
            text_content=extracted_text
        )
    ]

    meta = DocumentMetadata(
        document_id=doc_id,
        filename=filename,
        file_type="image/png" if filename.lower().endswith(".png") else "image/jpeg",
        file_size_bytes=file_size,
        page_count=1,
        upload_timestamp=upload_time,
        extraction_method="ocr_image" if not is_fallback else "fallback_extracted",
        ocr_confidence=confidence,
        extracted_text=extracted_text,
        needs_ocr_review=True,  # Users can review OCR results
        is_fictional_placeholder=("placeholder" in filename.lower() or "demo" in filename.lower()),
        verification_status="unverified"
    )
    return meta, chunks


def parse_document(file_path: str, filename: str) -> Tuple[DocumentMetadata, List[DocumentChunk]]:
    """Parse document based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        return parse_pdf_document(file_path, filename)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return parse_image_document(file_path, filename)
    else:
        raise ValueError(f"Unsupported format: {ext}")
