import re
import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.app.nlp.preprocessing import split_kannada_sentences, clean_kannada_text
from backend.app.nlp.stopwords_kn import get_kannada_stopwords

# Regex for Kannada tokens (preserving Indic unicode words of length >= 2)
KANNADA_WORD_PATTERN = re.compile(r'[\u0C80-\u0CFF\w]{2,}')

def tokenize_kannada_words(text: str) -> List[str]:
    """Tokenizes Kannada text into clean words, removing punctuation and numbers."""
    text = clean_kannada_text(text)
    words = KANNADA_WORD_PATTERN.findall(text)
    stopwords = get_kannada_stopwords()
    
    # Filter out pure digits and stopwords
    filtered_words = [
        w for w in words 
        if not w.isdigit() and w.lower() not in stopwords and len(w) > 1
    ]
    return filtered_words

def extract_kannada_keywords(text: str, top_n: int = 10) -> List[Dict[str, float]]:
    """
    Extracts top N keywords from Kannada document using TF-IDF, Term Frequency,
    and Positional Weighting.
    
    Formula:
    final_score = 0.60 * tfidf_score + 0.25 * frequency_score + 0.15 * position_score
    """
    sentences = split_kannada_sentences(text)
    if not sentences:
        return []

    tokens = tokenize_kannada_words(text)
    if not tokens:
        return []

    total_tokens = len(tokens)
    
    # Calculate Term Frequencies
    freq_dict = {}
    position_dict = {}
    for idx, token in enumerate(tokens):
        freq_dict[token] = freq_dict.get(token, 0) + 1
        if token not in position_dict:
            # Position score: earlier tokens get higher positional weight (decaying)
            position_dict[token] = 1.0 - (idx / total_tokens)

    # Build sentence documents for TF-IDF
    sentence_docs = []
    for s in sentences:
        s_tokens = tokenize_kannada_words(s)
        if s_tokens:
            sentence_docs.append(" ".join(s_tokens))

    tfidf_dict = {}
    if sentence_docs:
        try:
            vectorizer = TfidfVectorizer(token_pattern=r'[\u0C80-\u0CFF\w]{2,}')
            tfidf_matrix = vectorizer.fit_transform(sentence_docs)
            feature_names = vectorizer.get_feature_names_out()
            # Mean TF-IDF score across sentences
            mean_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
            for word, score in zip(feature_names, mean_tfidf):
                tfidf_dict[word] = float(score)
        except Exception:
            # Fallback if TF-IDF matrix creation fails
            tfidf_dict = {w: freq_dict[w] / total_tokens for w in freq_dict}

    # Normalize metrics to [0, 1] range
    max_freq = max(freq_dict.values()) if freq_dict else 1
    max_tfidf = max(tfidf_dict.values()) if tfidf_dict and max(tfidf_dict.values()) > 0 else 1

    scored_keywords = []
    for word, freq in freq_dict.items():
        norm_freq = freq / max_freq
        norm_tfidf = tfidf_dict.get(word, 0.0) / max_tfidf
        pos_score = position_dict.get(word, 0.5)

        # Composite score calculation
        composite_score = (0.60 * norm_tfidf) + (0.25 * norm_freq) + (0.15 * pos_score)
        scored_keywords.append({
            "word": word,
            "score": round(float(composite_score), 4)
        })

    # Sort descending by composite score
    scored_keywords.sort(key=lambda x: x["score"], reverse=True)
    return scored_keywords[:top_n]
