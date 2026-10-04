import logging
import torch
from typing import List, Dict
from backend.app.nlp.preprocessing import (
    split_kannada_sentences,
    clean_kannada_text,
    validate_kannada_text
)
from backend.app.nlp.keywords import tokenize_kannada_words
from backend.app.nlp.sentence_ranker import rank_important_sentences
from backend.app.services.model_loader import model_manager

logger = logging.getLogger("KannadaSaar.Summarizer")

# Default summary length thresholds in target output tokens
LENGTH_CONFIGS = {
    "short": {"min_length": 25, "max_length": 65, "ratio": 0.25},
    "medium": {"min_length": 45, "max_length": 120, "ratio": 0.35},
    "detailed": {"min_length": 75, "max_length": 220, "ratio": 0.50}
}

def chunk_text(text: str, max_words_per_chunk: int = 140) -> List[str]:
    """
    Hierarchical Long Document Strategy:
    Splits long documents into manageable chunks at Kannada sentence boundaries
    to respect transformer model token limits (~512 subwords).
    """
    sentences = split_kannada_sentences(text)
    if not sentences:
        return [text]

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = len(tokenize_kannada_words(sentence)) or len(sentence.split())
        if current_word_count + sentence_words > max_words_per_chunk and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_words
        else:
            current_chunk.append(sentence)
            current_word_count += sentence_words

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def _generate_extractive_fallback_summary(text: str, target_ratio: float = 0.35) -> str:
    """Generates a high-quality extractive summary using sentence ranking as fallback."""
    sentences = split_kannada_sentences(text)
    if len(sentences) <= 2:
        return text.strip()

    target_count = max(1, int(len(sentences) * target_ratio))
    ranked = rank_important_sentences(text, top_k=target_count)
    summary_sentences = [r["sentence"] for r in ranked]
    return " ".join(summary_sentences)

def _summarize_single_chunk(chunk_text_str: str, length_mode: str, model, tokenizer, device: str) -> str:
    """Summarizes a single text chunk using the Indic Seq2Seq Transformer model."""
    try:
        config = LENGTH_CONFIGS.get(length_mode.lower(), LENGTH_CONFIGS["medium"])
        
        # Format input text with Kannada language tag prefix if supported
        input_prompt = f"<2kn> {chunk_text_str}"
        
        inputs = tokenizer(
            input_prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(device)

        with torch.inference_mode():
            summary_ids = model.generate(
                inputs["input_ids"],
                num_beams=4,
                length_penalty=1.0,
                max_length=config["max_length"],
                min_length=config["min_length"],
                no_repeat_ngram_size=3,
                early_stopping=True
            )

        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return clean_kannada_text(summary_text)
    except Exception as e:
        logger.warning(f"Error during seq2seq generation for chunk: {str(e)}. Using fallback.")
        config = LENGTH_CONFIGS.get(length_mode.lower(), LENGTH_CONFIGS["medium"])
        return _generate_extractive_fallback_summary(chunk_text_str, target_ratio=config["ratio"])

def summarize_text(text: str, summary_length: str = "medium") -> Dict[str, any]:
    """
    Main Summarization Engine Pipeline:
    1. Language Validation
    2. Hierarchical Document Chunking
    3. Seq2Seq Model Inference / Fallback Execution
    4. Multi-chunk Combination & Deduplication
    """
    clean_input = clean_kannada_text(text)
    is_valid, msg = validate_kannada_text(clean_input)
    if not is_valid:
        raise ValueError(msg)

    sentences = split_kannada_sentences(clean_input)
    # If text is extremely short, return as-is
    if len(sentences) <= 1:
        return {
            "summary": clean_input,
            "used_model": "direct_pass",
            "chunks_processed": 1
        }

    model, tokenizer, device, model_name = model_manager.get_model_and_tokenizer()
    
    # Check if extractive engine is requested or active
    if model_manager.use_fallback_extractive or model is None or tokenizer is None:
        config = LENGTH_CONFIGS.get(summary_length.lower(), LENGTH_CONFIGS["medium"])
        fallback_summary = _generate_extractive_fallback_summary(clean_input, target_ratio=config["ratio"])
        return {
            "summary": fallback_summary,
            "used_model": "TF-IDF Extractive Fallback Engine",
            "chunks_processed": 1
        }

    # Split into chunks if document is long
    chunks = chunk_text(clean_input, max_words_per_chunk=140)
    chunk_summaries = []

    for chunk in chunks:
        chunk_summary = _summarize_single_chunk(chunk, summary_length, model, tokenizer, device)
        if chunk_summary and chunk_summary not in chunk_summaries:
            chunk_summaries.append(chunk_summary)

    combined_summary = " ".join(chunk_summaries)

    # If combined summary from multiple chunks is still too long, perform second-pass summarization
    if len(chunks) > 2:
        combined_summary = _generate_extractive_fallback_summary(
            combined_summary,
            target_ratio=0.60
        )

    # Post-processing sentence deduplication
    final_sentences = []
    for s in split_kannada_sentences(combined_summary):
        if s not in final_sentences:
            final_sentences.append(s)

    return {
        "summary": " ".join(final_sentences),
        "used_model": model_name,
        "chunks_processed": len(chunks)
    }
