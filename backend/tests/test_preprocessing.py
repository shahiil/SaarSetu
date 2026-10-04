from backend.app.nlp.preprocessing import (
    clean_kannada_text,
    split_kannada_sentences,
    validate_kannada_text,
    calculate_kannada_ratio
)
from backend.app.nlp.stopwords_kn import get_kannada_stopwords

def test_kannada_cleaning():
    raw_text = "  ಬೆಂಗಳೂರು   ಕರ್ನಾಟಕದ  ರಾಜಧಾನಿ.  "
    cleaned = clean_kannada_text(raw_text)
    assert cleaned == "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ."

def test_sentence_segmentation():
    text = "ಕರ್ನಾಟಕವು ಭಾರತದ ಪ್ರಮುಖ ರಾಜ್ಯಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ. ಬೆಂಗಳೂರನ್ನು ಭಾರತದ ತಂತ್ರಜ್ಞಾನ ರಾಜಧಾನಿ ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ!"
    sentences = split_kannada_sentences(text)
    assert len(sentences) == 2
    assert "ಕರ್ನಾಟಕವು" in sentences[0]
    assert "ಬೆಂಗಳೂರನ್ನು" in sentences[1]

def test_language_validation():
    kannada_text = "ಬೆಂಗಳೂರು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಪ್ರಸಿದ್ಧವಾಗಿದೆ."
    is_valid, msg = validate_kannada_text(kannada_text)
    assert is_valid is True
    
    english_text = "Bengaluru is the capital city of Karnataka state in India."
    is_valid_en, msg_en = validate_kannada_text(english_text)
    assert is_valid_en is False
    assert "ದಯವಿಟ್ಟು" in msg_en

def test_stopwords():
    stopwords = get_kannada_stopwords()
    assert "ಮತ್ತು" in stopwords
    assert "ಆದರೆ" in stopwords
    assert len(stopwords) > 30

if __name__ == "__main__":
    test_kannada_cleaning()
    test_sentence_segmentation()
    test_language_validation()
    test_stopwords()
    print("All preprocessing and language detection tests passed successfully!")
