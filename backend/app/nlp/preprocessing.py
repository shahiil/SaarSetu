import re
from typing import List, Tuple
from backend.app.nlp.language import calculate_kannada_ratio, detect_kannada_language

# Common Kannada abbreviations that should not trigger sentence splits
KANNADA_ABBREVIATIONS = [
    r'ಡಾ\.', r'ಪ್ರೊ\.', r'ಶ್ರೀ\.', r'ಶ್ರೀಮತಿ\.', r'ಇ\.', r'ಸ\.', r'ಐ\.ಟಿ\.', r'ಎ\.ಐ\.'
]

def normalize_whitespace(text: str) -> str:
    """Collapses multiple spaces, tabs, and unnecessary line breaks into clean text."""
    if not text:
        return ""
    # Replace multiple newlines with single newline
    text = re.sub(r'\n+', '\n', text)
    # Replace tabs and multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def remove_unwanted_characters(text: str) -> str:
    """
    Removes garbage/control characters while strictly preserving Kannada Unicode range,
    alphanumerics, standard punctuation, and sentence delimiters.
    """
    if not text:
        return ""
    # Keep printable characters, Kannada unicode (0C80-0CFF), punctuation, and whitespace
    # Replace control characters and unprintable symbols
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    return text

def normalize_kannada_text(text: str) -> str:
    """Normalizes Kannada Unicode variants and removes extra whitespace."""
    if not text:
        return ""
    text = remove_unwanted_characters(text)
    text = normalize_whitespace(text)
    return text

def clean_kannada_text(text: str) -> str:
    """Full preprocessing pipeline for raw user input Kannada text."""
    return normalize_kannada_text(text)

def split_kannada_sentences(text: str) -> List[str]:
    """
    Splits Kannada text into sentences based on Kannada and standard punctuation:
    Full stop (.), Exclamation (!), Question mark (?), Danda (।), Double Danda (॥), and Newlines.
    Handles abbreviations gracefully.
    """
    text = clean_kannada_text(text)
    if not text:
        return []

    # Protect abbreviations by temporarily replacing dots with a unique token
    protected_text = text
    for i, abbr in enumerate(KANNADA_ABBREVIATIONS):
        protected_text = re.sub(abbr, f"__ABBR_{i}__", protected_text)

    # Regex pattern for sentence boundaries: ., ?, !, ।, ॥ or newlines
    sentence_delimiters = re.compile(r'(?<=[.?!।॥\n])\s+')
    raw_sentences = sentence_delimiters.split(protected_text)
    
    sentences = []
    for s in raw_sentences:
        # Restore abbreviations
        for i in range(len(KANNADA_ABBREVIATIONS)):
            s = s.replace(f"__ABBR_{i}__", KANNADA_ABBREVIATIONS[i].replace(r'\.', '.'))
        
        s = s.strip()
        if len(s) > 1:  # Ignore trivial 1-character artifacts
            sentences.append(s)
            
    # Fallback if delimiter split yields only 1 block but newlines exist
    if len(sentences) <= 1 and '\n' in text:
        sentences = [p.strip() for p in text.split('\n') if p.strip()]
        
    return sentences if sentences else [text]

def validate_kannada_text(text: str, threshold: float = 0.40) -> Tuple[bool, str]:
    """
    Validates if input text is valid Kannada.
    Returns (is_valid, user_friendly_message).
    """
    detection = detect_kannada_language(text, threshold=threshold)
    return detection["is_kannada"], detection["message"]
