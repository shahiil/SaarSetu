from backend.app.nlp.keywords import extract_kannada_keywords
from backend.app.nlp.sentence_ranker import rank_important_sentences
from backend.app.nlp.statistics import calculate_text_statistics

SAMPLE_TEXT = (
    "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಮಾತ್ರವಲ್ಲದೆ, ಭಾರತದ ಅತ್ಯಂತ ಪ್ರಮುಖ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ. "
    "ಜಾಗತಿಕ ಮಟ್ಟದಲ್ಲಿ ಇದನ್ನು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ. "
    "ನೂರಾರು ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ (IT) ಸಂಸ್ಥೆಗಳು, ಉದ್ಯಮಗಳು ಮತ್ತು ನವೋದ್ಯಮಗಳು (Startups) ಇಲ್ಲಿ ತಮ್ಮ ಕೇಂದ್ರ ಕಚೇರಿಗಳನ್ನು ಹೊಂದಿವೆ. "
    "ಎಲೆಕ್ಟ್ರಾನಿಕ್ ಸಿಟಿ, ವೈಟ್‌ಫೀಲ್ಡ್, ಮಾನ್ಯತಾ ಟೆಕ್ ಪಾರ್ಕ್ ನಂತಹ ಬೃಹತ್ ತಂತ್ರಜ್ಞಾನ ಪಾರ್ಕ್‌ಗಳು ನಗರದಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿವೆ."
)

SAMPLE_SUMMARY = "ಬೆಂಗಳೂರು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಪ್ರಸಿದ್ಧವಾದ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ."

def test_keywords():
    keywords = extract_kannada_keywords(SAMPLE_TEXT, top_n=5)
    assert len(keywords) > 0
    words = [k["word"] for k in keywords]
    assert "ಬೆಂಗಳೂರು" in words or "ತಂತ್ರಜ್ಞಾನ" in words

def test_sentence_ranker():
    sentences = rank_important_sentences(SAMPLE_TEXT, top_k=2)
    assert len(sentences) == 2
    assert "sentence" in sentences[0]
    assert "score" in sentences[0]

def test_statistics():
    stats = calculate_text_statistics(SAMPLE_TEXT, SAMPLE_SUMMARY)
    assert stats["original_words"] > stats["summary_words"]
    assert stats["compression_ratio"] > 0
    assert stats["original_sentences"] == 4

if __name__ == "__main__":
    test_keywords()
    test_sentence_ranker()
    test_statistics()
    print("All NLP module tests (Keywords, Sentence Ranker, Statistics) passed successfully!")
