# Dataset Documentation — IndicSentenceSummarization (Kannada Subset)

## Dataset Overview

The academic dataset component of **KannadaSaar** is derived from the **AI4Bharat IndicSentenceSummarization** benchmark dataset for Indic languages.

- **Source**: AI4Bharat / HuggingFace `ai4bharat/IndicSentenceSummarization`
- **Target Language**: Kannada (`kn`)
- **Task**: Abstractive Text Summarization & Sentence Compression
- **Data Format**: JSON Lines / CSV containing original documents (`document`) and reference summaries (`summary`).

## Data Directory Structure

```
data/
├── raw/                 # Downloaded raw dataset files
├── processed/           # Normalized Kannada samples
├── train/               # 80% Training subset
├── validation/          # 10% Validation subset
├── test/                # 10% Test evaluation subset
└── sample_articles.json # 5 Demonstration Kannada passages across domain categories
```

## Subset Statistics & Split

| Split      | Percentage | Sample Count (Subset) | Purpose |
|------------|------------|-----------------------|---------|
| Train      | 80%        | 800                   | Optional fine-tuning of sequence-to-sequence model |
| Validation | 10%        | 100                   | Checkpoint selection & loss monitoring |
| Test       | 10%        | 100                   | ROUGE evaluation vs baseline model |

## Preprocessing Applied

1. Removal of non-Indic non-punctuation control characters.
2. Normalization of whitespace and unicode diacritics.
3. Filtering out samples where Kannada script ratio is below 40%.
4. Truncation / sentence boundary alignment.
