# System Architecture — KannadaSaar

KannadaSaar is a full-stack Kannada Natural Language Processing (NLP) application designed for abstractive summarization, sentence segmentation, TF-IDF keyword extraction, and important sentence identification.

## High-Level Architecture Diagram

```
                              USER
                               │
                               ▼
                    ┌─────────────────────┐
                    │    React + Vite     │
                    │ Soft Neumorphism UI │
                    └──────────┬──────────┘
                               │ HTTP / REST API
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌──────────────┐       ┌──────────────┐       ┌─────────────────┐
│ Language     │       │ Sentence     │       │ Kannada         │
│ Validation   │       │ Segmentation │       │ Preprocessing   │
└──────┬───────┘       └──────┬───────┘       └────────┬────────┘
       │                      │                        │
       └──────────────────────┼────────────────────────┘
                              │
       ┌──────────────────────┼────────────────────────┐
       ▼                      ▼                        ▼
┌──────────────┐       ┌──────────────┐       ┌─────────────────┐
│ Abstractive  │       │ TF-IDF       │       │ Sentence        │
│ Summarizer   │       │ Keyword      │       │ Ranker          │
│ (IndicBART/  │       │ Extraction   │       │ (Extractive     │
│ MultiIndicSS)│       │ (Position+Freq)│     │ Baseline/Rank)  │
└──────┬───────┘       └──────┬───────┘       └────────┬────────┘
       │                      │                        │
       └──────────────────────┼────────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Statistics & Metrics │
                   │ Compression / Time   │
                   └──────────┬───────────┘
                              │
                              ▼
                    JSON Response Payload
```

## Core Pipeline Components

1. **Frontend (React + Vite)**:
   - Soft Neumorphic design aesthetic with Light/Dark mode.
   - Interactive summarization panel with configurable length (Short, Medium, Detailed).
   - Real-time statistics display (word count, sentence count, compression ratio, reading time).
   - Keyword tag visualizer with term relevance highlighting.
   - History persistence using browser `localStorage`.

2. **FastAPI Web Service**:
   - Pydantic schema validation.
   - Asynchronous request handling.
   - Comprehensive error wrapping (HTTP 400, 413, 422, 500).
   - CORS & Request security constraints.

3. **Kannada NLP Preprocessing**:
   - Kannada Unicode validation (`0x0C80` - `0x0CFF`).
   - Text normalization & garbage character removal.
   - Punctuation-aware Kannada sentence boundary disambiguation.

4. **Summarization Pipeline**:
   - Pretrained Indic sequence-to-sequence model: `ai4bharat/MultiIndicSentenceSummarizationSS` (or `ai4bharat/IndicBART`).
   - Hierarchical text chunking strategy for long documents exceeding maximum token window limits.
   - Beam search decoding with repetition penalties.

5. **Information Extraction**:
   - Custom TF-IDF keyword extractor incorporating word frequency and positional decay weights.
   - Extractive TF-IDF sentence scoring engine for important sentence extraction.

6. **Evaluation Subsystem**:
   - ROUGE-1, ROUGE-2, and ROUGE-L metric calculation against reference summaries.
   - Comparative benchmark against an extractive TF-IDF baseline.
