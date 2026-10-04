import logging
from typing import List
from deep_translator import GoogleTranslator, MyMemoryTranslator

logger = logging.getLogger("KannadaSaar.Translator")

def translate_kannada_to_english(text: str) -> str:
    """Translates a single Kannada string into English with multi-provider fallback."""
    if not text or not text.strip():
        return ""
    
    # 1. Try Google Translator
    try:
        translated = GoogleTranslator(source='kn', target='en').translate(text)
        if translated and translated.strip():
            return translated.strip()
    except Exception as e:
        logger.debug(f"GoogleTranslator single translation notice: {str(e)}")

    # 2. Fallback to MyMemory Translator
    try:
        translated = MyMemoryTranslator(source='kannada', target='english').translate(text)
        if translated and translated.strip() and "QUERY LENGTH LIMIT EXCEEDED" not in translated.upper():
            return translated.strip()
    except Exception as e:
        logger.debug(f"MyMemoryTranslator single translation notice: {str(e)}")

    return text.strip()

def translate_batch_kannada_to_english(texts: List[str]) -> List[str]:
    """
    Translates a list of Kannada strings into English using robust batch handling.
    Safely falls back per-item if batch rate limits occur.
    """
    if not texts:
        return []

    valid_texts = [t.strip() if t else "" for t in texts]
    if not any(valid_texts):
        return texts

    translated_results = []

    # 1. Try Google Translator batch
    try:
        results = GoogleTranslator(source='kn', target='en').translate_batch(valid_texts)
        if results and len(results) == len(texts):
            return [r if r else valid_texts[i] for i, r in enumerate(results)]
    except Exception as e:
        logger.warning(f"Batch translation rate-limit notice: {str(e)}. Switching to resilient per-item fallback.")

    # 2. Resilient per-item translation with graceful fallback
    for item in valid_texts:
        if not item:
            translated_results.append("")
        else:
            translated_results.append(translate_kannada_to_english(item))

    return translated_results
