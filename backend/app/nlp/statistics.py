from typing import Dict
from backend.app.nlp.preprocessing import split_kannada_sentences, clean_kannada_text
from backend.app.nlp.keywords import tokenize_kannada_words

def calculate_text_statistics(original_text: str, summary_text: str) -> Dict[str, any]:
    """
    Computes text length, word count, sentence count, compression ratio,
    and estimated reading time comparison.
    """
    clean_orig = clean_kannada_text(original_text)
    clean_summ = clean_kannada_text(summary_text)

    orig_chars = len(clean_orig)
    summ_chars = len(clean_summ)

    orig_sentences = len(split_kannada_sentences(clean_orig))
    summ_sentences = len(split_kannada_sentences(clean_summ)) if clean_summ else 0

    # Kannada word count using split & unicode word pattern
    orig_words = len(tokenize_kannada_words(clean_orig)) or len(clean_orig.split())
    summ_words = len(tokenize_kannada_words(clean_summ)) if clean_summ else 0
    if summary_text and summ_words == 0:
        summ_words = len(clean_summ.split())

    # Compression ratio calculation
    if orig_words > 0:
        compression = (1.0 - (summ_words / orig_words)) * 100.0
        compression = max(0.0, min(100.0, compression))
    else:
        compression = 0.0

    # Indic reading speed: ~150-180 words per minute
    reading_speed_wpm = 180.0
    reading_time_before = round(orig_words / reading_speed_wpm, 1)
    reading_time_after = round(summ_words / reading_speed_wpm, 1)

    return {
        "original_characters": orig_chars,
        "summary_characters": summ_chars,
        "original_words": orig_words,
        "summary_words": summ_words,
        "original_sentences": orig_sentences,
        "summary_sentences": summ_sentences,
        "compression_ratio": round(compression, 1),
        "reading_time_before": max(0.1, reading_time_before) if orig_words > 0 else 0.0,
        "reading_time_after": reading_time_after
    }
