from pydantic import BaseModel, Field
from typing import List, Optional

class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Kannada article or passage to summarize")
    summary_length: Optional[str] = Field("medium", description="Desired summary length: short, medium, or detailed")
    keyword_count: Optional[int] = Field(10, ge=3, le=20, description="Number of top keywords to extract")

class KeywordItem(BaseModel):
    word: str
    score: float
    word_english: Optional[str] = None

class ImportantSentenceItem(BaseModel):
    sentence: str
    score: float
    index: int
    sentence_english: Optional[str] = None

class StatisticsData(BaseModel):
    original_characters: int
    summary_characters: int
    original_words: int
    summary_words: int
    original_sentences: int
    summary_sentences: int
    compression_ratio: float
    reading_time_before: float
    reading_time_after: float

class SummarizeResponse(BaseModel):
    summary: str
    summary_english: Optional[str] = None
    keywords: List[KeywordItem]
    important_sentences: List[ImportantSentenceItem]
    statistics: StatisticsData
    language: str
    processing_time: float

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    language: str
    is_kannada: bool
    kannada_ratio: float
    character_count: int
    word_count: int
    sentence_count: int

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    device: str
    version: str
