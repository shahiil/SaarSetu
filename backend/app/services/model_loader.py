import os
import torch
import logging
from typing import Tuple, Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from backend.app.config import settings

logger = logging.getLogger("KannadaSaar.ModelLoader")

class ModelManager:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.loaded_model_name = ""
        self.is_loaded = False
        self.use_fallback_extractive = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance

    def load_model(self) -> bool:
        if self.is_loaded:
            return True

        # 1. Check for local custom fine-tuned checkpoint first
        local_checkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "model_checkpoints"))
        
        model_candidates = []
        if os.path.exists(local_checkpoint_dir) and any(f for f in os.listdir(local_checkpoint_dir) if f.endswith(('.bin', '.safetensors'))):
            logger.info(f"Found local fine-tuned model checkpoint at: {local_checkpoint_dir}")
            model_candidates.append(local_checkpoint_dir)

        # 2. Add Hugging Face pretrained model candidates
        model_candidates.extend([
            settings.MODEL_NAME,
            settings.FALLBACK_MODEL_NAME
        ])

        logger.info(f"Initializing Model Loader. Target Device: {self.device}")

        for model_name in model_candidates:
            try:
                logger.info(f"Attempting to load model: {model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                self.model.to(self.device)
                self.model.eval()
                
                self.loaded_model_name = "Local Fine-Tuned Checkpoint" if model_name == local_checkpoint_dir else model_name
                self.is_loaded = True
                self.use_fallback_extractive = False
                logger.info(f"Successfully loaded model '{self.loaded_model_name}' on device '{self.device}'")
                return True
            except Exception as e:
                logger.warning(f"Failed to load model '{model_name}': {str(e)}")

        logger.warning("Could not load Hugging Face Seq2Seq model. Enabling lightweight TF-IDF Extractive fallback engine.")
        self.use_fallback_extractive = True
        self.loaded_model_name = "TF-IDF Extractive Engine (Fallback)"
        self.is_loaded = True
        return True

    def get_model_and_tokenizer(self) -> Tuple[Optional[any], Optional[any], str, str]:
        if not self.is_loaded:
            self.load_model()
        return self.model, self.tokenizer, self.device, self.loaded_model_name

model_manager = ModelManager.get_instance()

def get_model():
    return model_manager.get_model_and_tokenizer()
