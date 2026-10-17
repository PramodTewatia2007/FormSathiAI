from fastapi import APIRouter
from ..models import AskQuestionRequest, AskQuestionResponse
from ..retrieval import answer_question
from ..session_manager import session_manager

router = APIRouter(prefix="/api/ask", tags=["qa"])


@router.post("", response_model=AskQuestionResponse)
def ask_question_endpoint(req: AskQuestionRequest):
    """
    Answer questions grounded strictly in official instructions and session documents.
    Works 100% offline deterministically when no external LLM key is configured.
    """
    session = session_manager.get_session(req.session_id)
    response = answer_question(
        question=req.question,
        language=req.language,
        user_chunks=session.chunks
    )
    return response
