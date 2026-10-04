"""
Kannada Stopword List for NLP Tokenization & Keyword Extraction.
Contains common grammatical words, pronouns, conjunctions, prepositions, and auxiliaries.
"""

KANNADA_STOPWORDS = {
    # Conjunctions & Connectives
    "ಮತ್ತು", "ಆದರೆ", "ಅಥವಾ", "ಹಾಗೂ", "ಆದ್ದರಿಂದ", "ಏಕೆಂದರೆ", "ಆದಾಗ್ಯೂ", "ಆದರೂ",
    
    # Pronouns & Demonstratives
    "ಇದು", "ಅದು", "ಈ", "ಆ", "ಎಂದು", "ಒಂದು", "ಅವರು", "ಅವನ", "ಅವಳು", "ನಾವು", "ನೀವು",
    "ನನ್ನ", "ನಮ್ಮ", "ನಿಮ್ಮ", "ಅವರ", "ಅವುಗಳು", "ಇವುಗಳು", "ಯಾರು", "ಏನು", "ಯಾವ", "ಯಾವಾಗ",
    "ಎಲ್ಲಿ", "ಹೇಗೆ", "ಎಷ್ಟು", "ಅಲ್ಲಿ", "ಇಲ್ಲಿ", "ಇವನು", "ಇವಳು", "ತನ್ನ", "ತಮ್ಮ",
    
    # Case Endings & Postpositions
    "ಮೇಲೆ", "ಕೆಳಗೆ", "ಇಂದ", "ಗೆ", "ನಲ್ಲಿ", "ಬಗ್ಗೆ", "ಕುರಿತು", "ತನಕ", "ವರೆಗೆ", "ನಡುವೆ",
    "ಒಳಗೆ", "ಹೊರಗೆ", "ಜೊತೆಗೆ", "ವಿರುದ್ಧ", "ಮುಂದೆ", "ಹಿಂದೆ", "ಅಂತರ", "ಮೂಲಕ", "ಸರಿ",
    
    # Common Auxiliary Verbs & Functional Terms
    "ಇದೆ", "ಇವೆ", "ಇಲ್ಲ", "ಆಗಿದೆ", "ಆಗಿವೆ", "ಇತ್ತು", "ಇದ್ದಾರೆ", "ಮಾಡಿದರು", "ಮಾಡುತ್ತದೆ",
    "ಆಗಿ", "ಇದ್ದು", "ಇದ್ದುವು", "ಆಗಬಹುದು", "ಮಾಡಬಹುದು", "ಎಂಬ", "ಎನ್ನುವ", "ಎಂದು", "ಅಂದರೆ",
    
    # Quantifiers & General Function Words
    "ಎಲ್ಲಾ", "ಎಲ್ಲ", "ಕೆಲವು", "ಹಲವು", "ಹೆಚ್ಚು", "ಕಡಿಮೆ", "ಮಾತ್ರ", "ಮತ್ತೆ", "ಪುನಃ",
    "ಉದಾಹರಣೆಗೆ", "ಮೊದಲಾದ", "ಸೇರಿದಂತೆ", "ಪ್ರತಿಯೊಂದು", "ಅತ್ಯಂತ", "ಇತರ", "ಅನೇಕ"
}

def get_kannada_stopwords() -> set:
    """Returns the set of Kannada stopwords."""
    return KANNADA_STOPWORDS
