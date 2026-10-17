import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEMO_DATA_DIR = BASE_DIR / "demo_data"
TEMP_STORAGE_DIR = BASE_DIR / "temp_storage"

TEMP_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Tesseract configuration
TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if not os.path.exists(TESSERACT_CMD):
    TESSERACT_CMD = "tesseract"  # fallback to PATH

# File validation
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB
MAX_PDF_PAGES = 50
MAX_IMAGE_PIXELS = 40_000_000
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# LLM Configuration (Optional live provider, defaults to None for offline demo)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "offline")

# Constant fictional warning
FICTIONAL_DEMO_WARNING = "FICTIONAL DEMO — NOT AN OFFICIAL SCHOLARSHIP — NOT VALID FOR REAL APPLICATIONS."
