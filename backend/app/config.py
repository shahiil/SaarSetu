import os

class Settings:
    PROJECT_NAME: str = "KannadaSaar"
    TAGLINE: str = "Turn long Kannada text into meaningful summaries."
    VERSION: str = "1.0.0"
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "ai4bharat/MultiIndicSentenceSummarizationSS")
    FALLBACK_MODEL_NAME: str = "ai4bharat/IndicBART"
    
    # NLP Configuration
    MAX_INPUT_CHARS: int = int(os.getenv("MAX_INPUT_CHARS", "30000"))
    MIN_INPUT_CHARS: int = 30
    KANNADA_THRESHOLD: float = float(os.getenv("KANNADA_THRESHOLD", "0.40"))
    DEFAULT_KEYWORD_COUNT: int = 10
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

settings = Settings()
