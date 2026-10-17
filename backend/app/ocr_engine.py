import os
import shutil
import logging
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from .config import TESSERACT_CMD, MAX_IMAGE_PIXELS

logger = logging.getLogger(__name__)

# Configure pytesseract executable path
if os.path.exists(TESSERACT_CMD):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


def is_tesseract_available() -> bool:
    """Check if tesseract OCR executable is available and functioning."""
    try:
        ver = pytesseract.get_tesseract_version()
        return bool(ver)
    except Exception as e:
        logger.warning(f"Tesseract OCR check failed: {e}")
        return False


def preprocess_image_for_ocr(img: Image.Image) -> Image.Image:
    """Convert to grayscale and enhance contrast for accurate OCR extraction."""
    gray = img.convert('L')
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.8)
    return enhanced


def run_ocr_on_image(image_path: str) -> dict:
    """
    Run OCR on image file.
    Returns:
        dict: {
            "success": bool,
            "text": str,
            "confidence": float,
            "error": str or None,
            "is_fallback": bool
        }
    """
    if not os.path.exists(image_path):
        return {
            "success": False,
            "text": "",
            "confidence": 0.0,
            "error": f"Image file not found: {image_path}",
            "is_fallback": False
        }

    if not is_tesseract_available():
        return {
            "success": False,
            "text": "[OCR Engine Unavailable: Tesseract is not installed or configured on this system.]",
            "confidence": 0.0,
            "error": "Tesseract binary not found.",
            "is_fallback": True
        }

    try:
        with Image.open(image_path) as raw_img:
            if raw_img.width * raw_img.height > MAX_IMAGE_PIXELS:
                raise ValueError("Image dimensions exceed the supported processing limit.")
            processed = preprocess_image_for_ocr(raw_img)
            
            # Extract detailed data for confidence score
            data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
            confs = [float(c) for c in data.get('conf', []) if c != '-1' and c != -1]
            avg_conf = sum(confs) / len(confs) if confs else 0.0
            
            text = pytesseract.image_to_string(processed)
            clean_text = text.strip()
            
            return {
                "success": True,
                "text": clean_text,
                "confidence": round(avg_conf, 2),
                "error": None,
                "is_fallback": False
            }
    except Exception as e:
        logger.error(f"Error during OCR execution: {e}")
        return {
            "success": False,
            "text": "",
            "confidence": 0.0,
            "error": str(e),
            "is_fallback": True
        }
