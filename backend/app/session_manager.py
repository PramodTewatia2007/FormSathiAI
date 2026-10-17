import shutil
import hashlib
import threading
import time
from typing import Dict, List
from .models import ApplicationFormData, DocumentMetadata, DocumentChunk
from .demo_data import get_default_application
from .config import TEMP_STORAGE_DIR


class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.application_form: ApplicationFormData = get_default_application()
        self.documents: Dict[str, DocumentMetadata] = {}
        self.chunks: List[DocumentChunk] = []
        self.document_attachments: Dict[str, List[tuple[str, object]]] = {}
        self.attachment_sources: Dict[str, List[tuple[str, object]]] = {}
        self.attachment_baselines: Dict[str, object] = {}
        self.consent_given: bool = False
        self.last_accessed = time.monotonic()
        # Session IDs arrive from the client. Never use them directly as paths.
        storage_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
        self.session_dir = TEMP_STORAGE_DIR / storage_key
        self.document_paths: Dict[str, str] = {}
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def reset(self):
        self.application_form = get_default_application()
        self.documents.clear()
        self.chunks.clear()
        self.document_paths.clear()
        self.document_attachments.clear()
        self.attachment_sources.clear()
        self.attachment_baselines.clear()
        self.consent_given = False
        if self.session_dir.exists():
            shutil.rmtree(self.session_dir, ignore_errors=True)
            self.session_dir.mkdir(parents=True, exist_ok=True)


class SessionManager:
    SESSION_TTL_SECONDS = 12 * 60 * 60
    MAX_SESSIONS = 500

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}
        self._lock = threading.RLock()

    def _remove_idle_sessions(self, now: float) -> None:
        expired = [
            key for key, session in self._sessions.items()
            if now - session.last_accessed > self.SESSION_TTL_SECONDS
        ]
        for key in expired:
            self._sessions.pop(key).reset()

    def get_session(self, session_id: str = "default_session") -> SessionState:
        now = time.monotonic()
        with self._lock:
            self._remove_idle_sessions(now)
            session = self._sessions.get(session_id)
            if session is None:
                if len(self._sessions) >= self.MAX_SESSIONS:
                    oldest_id = min(self._sessions, key=lambda key: self._sessions[key].last_accessed)
                    self._sessions.pop(oldest_id).reset()
                session = SessionState(session_id)
                self._sessions[session_id] = session
            session.last_accessed = now
            return session

    def reset_session(self, session_id: str = "default_session") -> SessionState:
        session = self.get_session(session_id)
        session.reset()
        session.last_accessed = time.monotonic()
        return session


session_manager = SessionManager()
