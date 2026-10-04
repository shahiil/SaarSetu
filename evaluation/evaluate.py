import os
import json
import pandas as pd
from rouge_score import rouge_scorer
from backend.app.nlp.summarizer import summarize_text, _generate_extractive_fallback_summary

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_DATA_PATH = os.path.join(BASE_DIR, "data", "test", "kannada_test.json")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
RESULTS_CSV = os.path.join(EVAL_DIR, "results.csv")
RESULTS_JSON = os.path.join(EVAL_DIR, "results.json")

def evaluate_summarization_models():
    print("=" * 60)
    print("KannadaSaar Academic Evaluation Suite (ROUGE Benchmarking)")
    print("=" * 60)

    if not os.path.exists(TEST_DATA_PATH):
        print(f"Error: Test dataset not found at {TEST_DATA_PATH}")
        print("Please run 'python training/preprocess_dataset.py' first.")
        return

    with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
        test_samples = json.load(f)

    print(f"Loaded {len(test_samples)} test samples from {TEST_DATA_PATH}\n")

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)

    baseline_scores = {"rouge1": [], "rouge2": [], "rougeL": []}
    abstractive_scores = {"rouge1": [], "rouge2": [], "rougeL": []}

    evaluation_records = []

    for idx, sample in enumerate(test_samples, 1):
        doc = sample["document"]
        ref_summ = sample["summary"]

        # 1. Extractive Baseline Summary
        extractive_summ = _generate_extractive_fallback_summary(doc, target_ratio=0.35)

        # 2. Indic Abstractive Model Summary
        try:
            abs_res = summarize_text(doc, summary_length="medium")
            abstractive_summ = abs_res["summary"]
        except Exception as e:
            print(f"Warning: Abstractive generation failed for sample {idx}. Using fallback.")
            abstractive_summ = extractive_summ

        # Compute ROUGE for Baseline
        score_base = scorer.score(ref_summ, extractive_summ)
        # Compute ROUGE for Abstractive
        score_abs = scorer.score(ref_summ, abstractive_summ)

        for key in ['rouge1', 'rouge2', 'rougeL']:
            baseline_scores[key].append(score_base[key].fmeasure)
            abstractive_scores[key].append(score_abs[key].fmeasure)

        record = {
            "id": sample.get("id", f"sample_{idx}"),
            "document_len": len(doc),
            "ref_summary": ref_summ,
            "extractive_summary": extractive_summ,
            "abstractive_summary": abstractive_summ,
            "baseline_rouge1_f1": round(score_base['rouge1'].fmeasure, 4),
            "baseline_rouge2_f1": round(score_base['rouge2'].fmeasure, 4),
            "baseline_rougeL_f1": round(score_base['rougeL'].fmeasure, 4),
            "abstractive_rouge1_f1": round(score_abs['rouge1'].fmeasure, 4),
            "abstractive_rouge2_f1": round(score_abs['rouge2'].fmeasure, 4),
            "abstractive_rougeL_f1": round(score_abs['rougeL'].fmeasure, 4),
        }
        evaluation_records.append(record)

    # Compute Averages
    def avg(lst):
        return round(sum(lst) / len(lst), 4) if lst else 0.0

    summary_metrics = {
        "dataset_samples": len(test_samples),
        "extractive_baseline": {
            "rouge1_f1": avg(baseline_scores['rouge1']),
            "rouge2_f1": avg(baseline_scores['rouge2']),
            "rougeL_f1": avg(baseline_scores['rougeL']),
        },
        "indic_abstractive_model": {
            "rouge1_f1": avg(abstractive_scores['rouge1']),
            "rouge2_f1": avg(abstractive_scores['rouge2']),
            "rougeL_f1": avg(abstractive_scores['rougeL']),
        }
    }

    # Save to JSON & CSV
    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "metrics_summary": summary_metrics,
            "detailed_records": evaluation_records
        }, f, ensure_ascii=False, indent=2)

    pd.DataFrame(evaluation_records).to_csv(RESULTS_CSV, index=False, encoding="utf-8")

    print("SUMMARY RESULTS:")
    print("-" * 50)
    print(f"{'Model Architecture':<30} | {'ROUGE-1':<8} | {'ROUGE-2':<8} | {'ROUGE-L':<8}")
    print("-" * 50)
    print(f"{'Extractive TF-IDF Baseline':<30} | {summary_metrics['extractive_baseline']['rouge1_f1']:<8.4f} | {summary_metrics['extractive_baseline']['rouge2_f1']:<8.4f} | {summary_metrics['extractive_baseline']['rougeL_f1']:<8.4f}")
    print(f"{'Indic Seq2Seq Abstractive':<30} | {summary_metrics['indic_abstractive_model']['rouge1_f1']:<8.4f} | {summary_metrics['indic_abstractive_model']['rouge2_f1']:<8.4f} | {summary_metrics['indic_abstractive_model']['rougeL_f1']:<8.4f}")
    print("-" * 50)
    print(f"\nSaved evaluation metrics to:")
    print(f" - JSON: {RESULTS_JSON}")
    print(f" - CSV:  {RESULTS_CSV}")

if __name__ == "__main__":
    evaluate_summarization_models()
