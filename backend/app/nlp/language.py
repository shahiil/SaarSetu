import re
from typing import Dict, Tuple

# Kannada Unicode block range: U+0C80 to U+0CFF
KANNADA_UNICODE_PATTERN = re.compile(r'[\u0C80-\u0CFF]')
ALPHANUMERIC_PATTERN = re.compile(r'[\w]', re.UNICODE)

def calculate_kannada_ratio(text: str) -> float:
    """Calculates the ratio of Kannada script characters relative to all alphabetic characters."""
    if not text or not text.strip():
        return 0.0
    
    kannada_chars = len(KANNADA_UNICODE_PATTERN.findall(text))
    # Count all alphabetic characters (excluding whitespace and pure ASCII punctuation)
    alpha_chars = sum(1 for c in text if c.isalnum())
    
    if alpha_chars == 0:
        return 0.0
    
    return kannada_chars / alpha_chars

def detect_kannada_language(text: str, threshold: float = 0.40) -> Dict[str, any]:
    """
    Detects language characteristics of input text.
    Returns language code ('kn', 'mixed', 'unknown') and metrics.
    """
    if not text or not text.strip():
        return {
            "language": "unknown",
            "is_kannada": False,
            "kannada_ratio": 0.0,
            "message": "ಪಠ್ಯವು ಖಾಲಿಯಾಗಿದೆ (Text is empty)."
        }
    
    ratio = calculate_kannada_ratio(text)
    
    if ratio >= threshold:
        lang = "kn"
        is_kn = True
        msg = "ಕನ್ನಡ ಪಠ್ಯ (Valid Kannada Text)."
    elif ratio > 0.15:
        lang = "mixed"
        is_kn = True  # Accept mixed text if significant Kannada presence exists
        msg = "ಮಿಶ್ರ ಪಠ್ಯ (Mixed Kannada-English Text)."
    else:
        lang = "unknown"
        is_kn = False
        msg = "ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ (Please enter Kannada text)."
        
    return {
        "language": lang,
        "is_kannada": is_kn,
        "kannada_ratio": round(ratio, 4),
        "message": msg
    }
