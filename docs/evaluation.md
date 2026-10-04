# Evaluation Methodology & Metrics — KannadaSaar

## ROUGE Evaluation Framework

To evaluate summarization quality quantitatively, **KannadaSaar** compares model-generated summaries against ground-truth reference summaries from the test dataset using the ROUGE metrics (Recall-Oriented Understudy for Gisting Evaluation).

### Evaluated Metrics

1. **ROUGE-1**: Overlap of unigrams (single words) between generated and reference summaries.
2. **ROUGE-2**: Overlap of bigrams (two-word sequences) measuring fluency.
3. **ROUGE-L**: Longest Common Subsequence (LCS) measuring structural similarity.

## Comparative Baseline Model

An **Extractive TF-IDF Baseline** is implemented in `evaluation/evaluate.py`:
- Calculates TF-IDF vectors for all sentences in the source document.
- Ranks sentences based on average TF-IDF word weights.
- Selects the top $N$ highest scoring sentences in original sentence order.

The evaluation script runs both the **Abstractive Indic Transformer** model and the **Extractive TF-IDF Baseline** on the Kannada test dataset and writes metrics to `evaluation/results.csv` and `evaluation/results.json`.
