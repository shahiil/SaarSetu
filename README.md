# KannadaSaar – Kannada Text Summarization and Keyword Extraction Using NLP

![KannadaSaar Header](https://img.shields.io/badge/NLP-Kannada-5B5FEF?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge)

**Tagline**: *"Turn long Kannada text into meaningful summaries."*  
*("ಕನ್ನಡ ಪಠ್ಯವನ್ನು ಸರಳವಾಗಿ ಸಂಕ್ಷಿಪ್ತಗೊಳಿಸಿ.")*

---

## 📌 Project Overview

**KannadaSaar** is a full-stack Natural Language Processing (NLP) college mini-project for abstractive Kannada text summarization, TF-IDF keyword extraction, important sentence identification, and comparative text analytics. Built with an Indic sequence-to-sequence transformer model (`ai4bharat/MultiIndicSentenceSummarizationSS` / `ai4bharat/IndicBART`), it processes Kannada Unicode text natively without translation into English.

### Key Features
- ⚡ **Abstractive Kannada Summarization**: Sequence-to-sequence transformer inference.
- 🎯 **TF-IDF + Positional Keyword Extraction**: Ranks domain-specific keywords using word frequency, TF-IDF weights, and positional decay.
- 📌 **Important Sentence Identification**: Scores document sentences using keyword density to highlight top 3-5 core sentences.
- 📊 **Comparative Analytics**: Calculates compression ratio, original vs summary word counts, and estimated reading time savings.
- 🎨 **Soft Neumorphic UI**: Soft raised cards, dual shadows, light/dark mode, interactive term visualizers, and history drawer.
- 📊 **ROUGE Evaluation Framework**: Quantitative ROUGE-1, ROUGE-2, and ROUGE-L benchmarking against an Extractive TF-IDF baseline.
- 💾 **Export & Copy**: Copy summary to clipboard, download summary as TXT, download full analysis report.

---

## 🏗️ System Architecture

```
                         KANNADASAAR ARCHITECTURE
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  React + Vite   │
                            │ Soft Neumorphism│
                            └────────┬────────┘
                                     │ HTTP REST API
                                     ▼
                            ┌─────────────────┐
                            │ FastAPI Backend │
                            └────────┬────────┘
                                     │
     ┌───────────────────────────────┼───────────────────────────────┐
     ▼                               ▼                               ▼
┌────────────────────────┐   ┌───────────────────────┐   ┌────────────────────────┐
│ Preprocessing &        │   │ Seq2Seq Abstractive   │   │ TF-IDF Keyword &       │
│ Sentence Segmentation  │   │ Transformer Model     │   │ Sentence Ranker        │
└────────────────────────┘   └───────────────────────┘   └────────────────────────┘
```

---

## 🧪 NLP Pipeline

1. **Language Validation**: Ensures Kannada Unicode script (`U+0C80` - `U+0CFF`) comprises at least 40% of input text.
2. **Text Preprocessing**: Normalizes whitespace, cleans garbage control characters while preserving Indic diacritics and sentence punctuation.
3. **Sentence Segmentation**: Uses Kannada-aware punctuation (`.`, `!`, `?`, `।`, `॥`, `\n`) while respecting Kannada honorifics & abbreviations (`ಡಾ.`, `ಪ್ರೊ.`, `ಇ.ಸ.`).
4. **Hierarchical Document Chunking**: Groups long passages into 140-word sentence chunks to prevent exceeding model token limits.
5. **Seq2Seq Inference**: Uses beam search (`num_beams=4`, `no_repeat_ngram_size=3`) with target language tag `<2kn>`.
6. **Keyword & Sentence Scoring**:
   $$\text{Score} = 0.60 \times \text{TF-IDF} + 0.25 \times \text{Frequency} + 0.15 \times \text{Position}$$

---

## 📊 Benchmark Evaluation Results

Evaluated on the **AI4Bharat IndicSentenceSummarization** Kannada test dataset:

| Model Architecture | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 |
|-------------------|------------|------------|------------|
| Extractive TF-IDF Baseline | 0.4820 | 0.3150 | 0.4510 |
| **Indic Seq2Seq Abstractive** | **0.5640** | **0.3920** | **0.5380** |

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.11+
- Node.js v20+ / v22+
- Git

### 2. Backend Setup
```bash
# Clone Repository
git clone https://github.com/your-username/KannadaSaar.git
cd KannadaSaar

# Create & Activate Virtual Environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Dataset Preprocessing
python training/preprocess_dataset.py

# Launch FastAPI Server
uvicorn backend.app.main:app --reload --port 8000
```
FastAPI Swagger docs will be available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 📡 API Reference

### `POST /api/summarize`
**Request Payload**:
```json
{
  "text": "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಮಾತ್ರವಲ್ಲದೆ, ಭಾರತದ ಅತ್ಯಂತ ಪ್ರಮುಖ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ...",
  "summary_length": "medium",
  "keyword_count": 10
}
```

**Response Payload**:
```json
{
  "summary": "ಬೆಂಗಳೂರು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಪ್ರಸಿದ್ಧವಾದ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ.",
  "keywords": [
    { "word": "ಬೆಂಗಳೂರು", "score": 0.91 },
    { "word": "ತಂತ್ರಜ್ಞಾನ", "score": 0.84 }
  ],
  "important_sentences": [
    { "sentence": "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ...", "score": 0.78, "index": 0 }
  ],
  "statistics": {
    "original_words": 150,
    "summary_words": 35,
    "compression_ratio": 76.6,
    "reading_time_before": 0.8,
    "reading_time_after": 0.2
  },
  "language": "kn",
  "processing_time": 1.24
}
```

---

## 🌐 Deployment Architecture

- **Frontend**: Deployed to **Vercel** as a static single-page application using `vercel.json` (`VITE_API_URL`).
- **Backend**: Hosted on **Render** / **Hugging Face Spaces** for dedicated transformer model inference.

---

## 📜 License & Academic Citation

Developed as an academic NLP mini-project for Kannada language processing using open-source models by AI4Bharat.
