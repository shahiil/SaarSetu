import os
import json
import torch
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import Dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KannadaSaar.Trainer")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRAIN_FILE = os.path.join(BASE_DIR, "data", "train", "kannada_train.json")
VAL_FILE = os.path.join(BASE_DIR, "data", "validation", "kannada_val.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "model_checkpoints")

def load_dataset_from_json(file_path: str) -> Dataset:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Dataset.from_list(data)

def train_kannada_model(
    model_name: str = "ai4bharat/MultiIndicSentenceSummarizationSS",
    epochs: int = 1,
    batch_size: int = 2
):
    print("=" * 60)
    print("KannadaSaar Sequence-to-Sequence Model Fine-Tuning Pipeline")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("\n[WARNING] GPU (CUDA) is not available! Training on CPU may be slow.")
    else:
        print(f"\n[INFO] CUDA detected: {torch.cuda.get_device_name(0)}")

    logger.info(f"Loading tokenizer & model weights from '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    train_dataset = load_dataset_from_json(TRAIN_FILE)
    val_dataset = load_dataset_from_json(VAL_FILE)

    def preprocess_function(examples):
        inputs = [f"<2kn> {doc}" for doc in examples["document"]]
        targets = [summ for summ in examples["summary"]]
        
        model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
        labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
        
        labels["input_ids"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in label]
            for label in labels["input_ids"]
        ]
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    print("Tokenizing train and validation splits...")
    tokenized_train = train_dataset.map(preprocess_function, batched=True)
    tokenized_val = val_dataset.map(preprocess_function, batched=True)

    training_args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        evaluation_strategy="epoch",
        learning_rate=3e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=epochs,
        predict_with_generate=True,
        fp16=(device == "cuda"),
        logging_dir="./logs",
        logging_steps=5,
        report_to="none"
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        tokenizer=tokenizer
    )

    print("\nStarting model fine-tuning...")
    trainer.train()

    print(f"\nSaving best fine-tuned model checkpoint to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Fine-tuning pipeline execution completed successfully!")

if __name__ == "__main__":
    train_kannada_model(epochs=1, batch_size=1)
