# Model Documentation — MultiIndicSentenceSummarizationSS / IndicBART

## Model Architecture

**KannadaSaar** utilizes an Indic-language pretrained Sequence-to-Sequence transformer model developed by AI4Bharat.

- **Primary Model**: `ai4bharat/MultiIndicSentenceSummarizationSS`
- **Alternative Model**: `ai4bharat/IndicBART`
- **Model Type**: Encoder-Decoder Transformer (Seq2Seq LM)
- **Tokenization**: SentencePiece multilingual BPE trained on Indic languages with special language tags (`<2kn>` for Kannada).

## Model Loading & Inference Optimization

1. **Singleton Model Loader**:
   - The model and tokenizer are loaded into memory once during FastAPI application startup.
   - Prevents redundant model reloading on every API request.

2. **Inference Execution**:
   - Executed under `torch.inference_mode()` with `model.eval()`.
   - Uses beam search decoding (`num_beams = 4`) and n-gram repetition penalty (`no_repeat_ngram_size = 3`).

3. **Hierarchical Document Chunking**:
   - For input documents exceeding max input tokens (~512 tokens), text is segmented at sentence boundaries into chunks.
   - Summaries are generated per chunk and merged recursively to ensure full document coverage without truncation.
