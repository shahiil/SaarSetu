import time
import logging
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import (
    SummarizeRequest,
    SummarizeResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    HealthResponse,
    KeywordItem,
    ImportantSentenceItem,
    StatisticsData
)
from backend.app.nlp.preprocessing import validate_kannada_text, clean_kannada_text, split_kannada_sentences
from backend.app.nlp.language import detect_kannada_language
from backend.app.nlp.keywords import extract_kannada_keywords, tokenize_kannada_words
from backend.app.nlp.sentence_ranker import rank_important_sentences
from backend.app.nlp.statistics import calculate_text_statistics
from backend.app.nlp.summarizer import summarize_text
from backend.app.nlp.translator import translate_kannada_to_english, translate_batch_kannada_to_english
from backend.app.services.model_loader import model_manager
from backend.app.config import settings

router = APIRouter(prefix="/api")
logger = logging.getLogger("KannadaSaar.API")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Returns application health status and model loader diagnostic state."""
    model, _, device, model_name = model_manager.get_model_and_tokenizer()
    return HealthResponse(
        status="ok",
        model_loaded=model_manager.is_loaded,
        model_name=model_name if model_name else "Not Loaded",
        device=device,
        version=settings.VERSION
    )

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_kannada_text(payload: AnalyzeRequest):
    """Performs light language validation and text metric analysis."""
    text = clean_kannada_text(payload.text)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ (Please enter Kannada text)."
        )

    detection = detect_kannada_language(text, threshold=settings.KANNADA_THRESHOLD)
    words = tokenize_kannada_words(text) or text.split()
    sentences = split_kannada_sentences(text)

    return AnalyzeResponse(
        language=detection["language"],
        is_kannada=detection["is_kannada"],
        kannada_ratio=detection["kannada_ratio"],
        character_count=len(text),
        word_count=len(words),
        sentence_count=len(sentences)
    )

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_kannada_article(payload: SummarizeRequest):
    """
    Main Kannada Natural Language Processing Endpoint:
    Executes Kannada validation, abstractive summarization, TF-IDF keyword extraction,
    important sentence ranking, comparative text statistics, and batch English translation.
    """
    start_time = time.time()
    raw_text = payload.text.strip() if payload.text else ""

    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ದಯವಿಟ್ಟು ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ (Please enter Kannada text)."
        )

    if len(raw_text) < settings.MIN_INPUT_CHARS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ಸಾರಾಂಶಕ್ಕಾಗಿ ಸ್ವಲ್ಪ ಹೆಚ್ಚು ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ (Text too short for meaningful summarization)."
        )

    if len(raw_text) > settings.MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"ನಮೂದಿಸಿದ ಪಠ್ಯವು ಗರಿಷ್ಠ ಮಿತಿಯನ್ನು ಮೀರಿದೆ (Text exceeds maximum threshold of {settings.MAX_INPUT_CHARS} characters)."
        )

    # 1. Kannada Language Validation
    is_kannada, error_msg = validate_kannada_text(raw_text, threshold=settings.KANNADA_THRESHOLD)
    if not is_kannada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    try:
        # 2. Text Summarization
        summarization_result = summarize_text(
            raw_text,
            summary_length=payload.summary_length or "medium"
        )
        generated_summary = summarization_result["summary"]

        # 3. Keyword Extraction (from original text)
        kw_count = payload.keyword_count or settings.DEFAULT_KEYWORD_COUNT
        raw_keywords = extract_kannada_keywords(raw_text, top_n=kw_count)

        # 4. Important Sentence Extraction (from original text)
        raw_sentences = rank_important_sentences(raw_text, top_k=3)

        # 5. Batch English Translation for (Summary + Keywords + Sentences)
        translation_batch = [generated_summary]
        for k in raw_keywords:
            translation_batch.append(k["word"])
        for s in raw_sentences:
            translation_batch.append(s["sentence"])

        translated_results = translate_batch_kannada_to_english(translation_batch)

        summary_english = translated_results[0] if translated_results else generated_summary
        kw_offset = 1
        kw_translated = translated_results[kw_offset : kw_offset + len(raw_keywords)]
        s_offset = kw_offset + len(raw_keywords)
        s_translated = translated_results[s_offset : s_offset + len(raw_sentences)]

        keywords_list = [
            KeywordItem(
                word=k["word"],
                score=k["score"],
                word_english=kw_translated[i] if i < len(kw_translated) else k["word"]
            )
            for i, k in enumerate(raw_keywords)
        ]

        important_sentences_list = [
            ImportantSentenceItem(
                sentence=s["sentence"],
                score=s["score"],
                index=s["index"],
                sentence_english=s_translated[i] if i < len(s_translated) else s["sentence"]
            )
            for i, s in enumerate(raw_sentences)
        ]

        # 6. Text Statistics Computation
        stats_dict = calculate_text_statistics(raw_text, generated_summary)
        statistics_obj = StatisticsData(**stats_dict)

        elapsed = round(time.time() - start_time, 2)

        return SummarizeResponse(
            summary=generated_summary,
            summary_english=summary_english,
            keywords=keywords_list,
            important_sentences=important_sentences_list,
            statistics=statistics_obj,
            language="kn",
            processing_time=elapsed
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during summarization processing pipeline: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ಸಾರಾಂಶ ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿ ಆಂತರಿಕ ದೋಷ ಸಂಭವಿಸಿದೆ (Internal NLP processing error)."
        )

@router.post("/extract-keywords")
async def extract_keywords_only(payload: SummarizeRequest):
    """Standalone keyword extraction endpoint."""
    raw_text = payload.text.strip() if payload.text else ""
    if not raw_text:
        raise HTTPException(status_code=400, detail="ಪಠ್ಯ ಖಾಲಿಯಾಗಿದೆ (Text is empty).")
    
    count = payload.keyword_count or 10
    keywords = extract_kannada_keywords(raw_text, top_n=count)
    return {"keywords": keywords}

@router.post("/extract-sentences")
async def extract_sentences_only(payload: SummarizeRequest):
    """Standalone important sentence extraction endpoint."""
    raw_text = payload.text.strip() if payload.text else ""
    if not raw_text:
        raise HTTPException(status_code=400, detail="ಪಠ್ಯ ಖಾಲಿಯಾಗಿದೆ (Text is empty).")
    
    sentences = rank_important_sentences(raw_text, top_k=3)
    return {"important_sentences": sentences}
