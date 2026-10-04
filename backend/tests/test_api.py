from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

SAMPLE_KANNADA_TEXT = (
    "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಮಾತ್ರವಲ್ಲದೆ, ಭಾರತದ ಅತ್ಯಂತ ಪ್ರಮುಖ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ. "
    "ಜಾಗತಿಕ ಮಟ್ಟದಲ್ಲಿ ಇದನ್ನು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ. "
    "ನೂರಾರು ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ (IT) ಸಂಸ್ಥೆಗಳು, ಉದ್ಯಮಗಳು ಮತ್ತು ನವೋದ್ಯಮಗಳು (Startups) ಇಲ್ಲಿ ತಮ್ಮ ಕೇಂದ್ರ ಕಚೇರಿಗಳನ್ನು ಹೊಂದಿವೆ. "
    "ಎಲೆಕ್ಟ್ರಾನಿಕ್ ಸಿಟಿ, ವೈಟ್‌ಫೀಲ್ಡ್, ಮಾನ್ಯತಾ ಟೆಕ್ ಪಾರ್ಕ್ ನಂತಹ ಬೃಹತ್ ತಂತ್ರಜ್ಞಾನ ಪಾರ್ಕ್‌ಗಳು ನಗರದಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿವೆ."
)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "KannadaSaar"

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_analyze():
    response = client.post("/api/analyze", json={"text": SAMPLE_KANNADA_TEXT})
    assert response.status_code == 200
    data = response.json()
    assert data["is_kannada"] is True
    assert data["word_count"] > 10

def test_summarize():
    response = client.post("/api/summarize", json={
        "text": SAMPLE_KANNADA_TEXT,
        "summary_length": "medium",
        "keyword_count": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert len(data["summary"]) > 0
    assert len(data["keywords"]) == 5
    assert len(data["important_sentences"]) > 0
    assert data["statistics"]["compression_ratio"] > 0

def test_invalid_language():
    response = client.post("/api/summarize", json={
        "text": "This is purely English text with no Kannada words at all.",
        "summary_length": "short"
    })
    assert response.status_code == 400
    assert "ದಯವಿಟ್ಟು" in response.json()["detail"]

if __name__ == "__main__":
    test_root()
    test_health()
    test_analyze()
    test_summarize()
    test_invalid_language()
    print("All FastAPI API tests passed successfully!")
