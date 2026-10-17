import os
import re
from typing import List, Optional, Tuple
from .models import DocumentChunk, SourceCitation, AskQuestionResponse
from .demo_data import EXACT_DEMO_QA, SCHOLARSHIP_RULES
from .config import FICTIONAL_DEMO_WARNING, DEMO_DATA_DIR
from .document_parser import parse_pdf_document

ABSENT_INFO_EN = "This information is not available in the provided instructions."
ABSENT_INFO_HI = "यह जानकारी दिए गए निर्देशों में उपलब्ध नहीं है।"


STOP_WORDS = {
    "what", "is", "the", "a", "an", "in", "to", "for", "of", "and", "or", "on", "at", 
    "are", "this", "that", "it", "with", "as", "by", "from", "be", "have", "has", "do",
    "does", "can", "could", "should", "would", "how", "why", "when", "where", "who",
    "क्या", "है", "की", "का", "के", "में", "से", "पर", "को", "और", "या", "यह", "वह"
}


def normalize_text(text: str) -> List[str]:
    """Tokenize and normalize text into clean words, excluding common stop words."""
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in cleaned.split() if len(w) > 2 and w not in STOP_WORDS]


class LocalDocumentStore:
    """Manages document chunks and retrieval for instructions and uploaded docs."""
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self._load_base_instructions()

    def _load_base_instructions(self):
        """Index default scholarship instructions if available."""
        inst_pdf = os.path.join(DEMO_DATA_DIR, "Udaan_Scholarship_Instructions_Demo.pdf")
        if os.path.exists(inst_pdf):
            try:
                _, parsed_chunks = parse_pdf_document(inst_pdf, "Udaan_Scholarship_Instructions_Demo.pdf")
                self.chunks.extend(parsed_chunks)
            except Exception as e:
                print(f"Warning: could not index instructions PDF: {e}")

    def search_chunks(
        self,
        query: str,
        top_k: int = 3,
        additional_chunks: Optional[List[DocumentChunk]] = None,
    ) -> List[Tuple[DocumentChunk, float]]:
        """Score base instructions and only the caller's session documents."""
        q_tokens = set(normalize_text(query))
        if not q_tokens:
            return []

        results = []
        for chunk in [*self.chunks, *(additional_chunks or [])]:
            chunk_tokens = set(normalize_text(chunk.text_content + " " + chunk.section_title))
            if not chunk_tokens:
                continue

            # Compute term overlap score
            matches = len(q_tokens.intersection(chunk_tokens))
            if matches == 0:
                continue

            score = matches / len(q_tokens)

            # Boost if section title specifically contains query words
            title_tokens = set(normalize_text(chunk.section_title))
            if q_tokens.intersection(title_tokens):
                score += 0.4

            if score >= 0.5:
                results.append((chunk, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


local_store = LocalDocumentStore()


def answer_question(
    question: str,
    language: str = "en",
    user_chunks: Optional[List[DocumentChunk]] = None
) -> AskQuestionResponse:
    """
    Answer question using grounded retrieval.
    Checks exact demo questions first, then checks local document store.
    If no source supports it, returns standard unavailable message.
    """
    clean_q = question.strip().lower()

    # 1. Check exact predefined demo questions
    for demo in EXACT_DEMO_QA:
        demo_en = demo["question_en"].lower()
        demo_hi = demo["question_hi"].lower()
        if demo_en in clean_q or clean_q in demo_en or demo_hi in clean_q or clean_q in demo_hi:
            answer_text = demo["answer_en"] if language == "en" else demo["answer_hi"]
            return AskQuestionResponse(
                question=question,
                language=language,
                answer=answer_text,
                source_citation=demo["citation"],
                is_live_ai=False,
                is_predefined_grounded=True,
                warning=FICTIONAL_DEMO_WARNING
            )

    # Keyword shortcuts for demo questions
    if any(k in clean_q for k in ["marks", "percentage", "qualifying", "अंक", "प्रतिशत"]):
        demo = EXACT_DEMO_QA[0]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )
    elif any(k in clean_q for k in ["income", "limit", "आय", "सीमा"]):
        demo = EXACT_DEMO_QA[1]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )
    elif any(k in clean_q for k in ["document", "documents", "list", "दस्तावेज", "कागजात"]):
        demo = EXACT_DEMO_QA[2]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )
    elif any(k in clean_q for k in ["deadline", "last date", "अंतिम तिथि", "डेटलाइन"]):
        demo = EXACT_DEMO_QA[3]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )
    elif any(k in clean_q for k in ["complete", "completed", "status", "पूर्ण", "पूरा"]):
        demo = EXACT_DEMO_QA[4]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )
    elif any(k in clean_q for k in ["real", "official", "fake", "असली", "वास्तविक"]):
        demo = EXACT_DEMO_QA[5]
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=demo["answer_en"] if language == "en" else demo["answer_hi"],
            source_citation=demo["citation"],
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )

    # 2. Search local store chunks
    hits = local_store.search_chunks(question, top_k=1, additional_chunks=user_chunks)
    if hits and hits[0][1] >= 0.35:
        best_chunk, score = hits[0]
        # Clean answer snippet from matching chunk
        lines = [line.strip() for line in best_chunk.text_content.split("\n") if line.strip()]
        snippet = " ".join(lines[:3])
        citation = SourceCitation(
            document_name=best_chunk.document_filename,
            page_number=best_chunk.page_number,
            section_heading=best_chunk.section_title,
            supporting_quote=snippet[:200]
        )
        ans = f"According to {best_chunk.section_title}: {snippet}" if language == "en" else f"{best_chunk.section_title} के अनुसार: {snippet}"
        return AskQuestionResponse(
            question=question,
            language=language,
            answer=ans,
            source_citation=citation,
            is_live_ai=False,
            is_predefined_grounded=True,
            warning=FICTIONAL_DEMO_WARNING
        )

    # 3. Information is absent from source documents: Strict grounding rule
    empty_citation = SourceCitation(
        document_name="Udaan_Scholarship_Instructions_Demo.pdf",
        page_number=None,
        section_heading="Information Not Found",
        supporting_quote=None
    )
    ans_text = ABSENT_INFO_EN if language == "en" else ABSENT_INFO_HI
    return AskQuestionResponse(
        question=question,
        language=language,
        answer=ans_text,
        source_citation=empty_citation,
        is_live_ai=False,
        is_predefined_grounded=True,
        warning=FICTIONAL_DEMO_WARNING
    )
