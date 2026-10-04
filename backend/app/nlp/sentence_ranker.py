from typing import List, Dict
from backend.app.nlp.preprocessing import split_kannada_sentences
from backend.app.nlp.keywords import extract_kannada_keywords, tokenize_kannada_words

def rank_important_sentences(text: str, top_k: int = 3) -> List[Dict[str, any]]:
    """
    Ranks document sentences based on keyword overlap, word density, and position score.
    Returns top K important sentences preserved in their original document order.
    """
    sentences = split_kannada_sentences(text)
    if not sentences:
        return []

    # Extract keywords with their relevance scores
    keywords = extract_kannada_keywords(text, top_n=15)
    keyword_weights = {k["word"]: k["score"] for k in keywords}

    scored_sentences = []
    total_sentences = len(sentences)

    for idx, sentence in enumerate(sentences):
        tokens = tokenize_kannada_words(sentence)
        if not tokens:
            continue

        # Sum keyword weights present in sentence
        kw_sum = sum(keyword_weights.get(token, 0.0) for token in tokens)
        
        # Sentence length normalization
        density_score = kw_sum / (len(tokens) + 1.0)
        
        # Position weight: first and last sentences often carry core summary information
        position_weight = 1.0
        if idx == 0:
            position_weight = 1.3
        elif idx == total_sentences - 1:
            position_weight = 1.1
        elif idx < total_sentences * 0.3:
            position_weight = 1.15

        final_score = (density_score * 0.75 + kw_sum * 0.25) * position_weight

        scored_sentences.append({
            "sentence": sentence,
            "score": round(float(final_score), 4),
            "index": idx
        })

    # Sort descending by score to pick top K
    sorted_sentences = sorted(scored_sentences, key=lambda x: x["score"], reverse=True)[:top_k]
    
    # Re-sort by original sentence index to maintain narrative coherence
    sorted_sentences.sort(key=lambda x: x["index"])

    return sorted_sentences
