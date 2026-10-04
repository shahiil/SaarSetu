import os
import json
import argparse
import urllib.request
import pandas as pd
from typing import List, Dict
from backend.app.nlp.preprocessing import clean_kannada_text, calculate_kannada_ratio

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "validation")
TEST_DIR = os.path.join(DATA_DIR, "test")

for d in [RAW_DIR, PROCESSED_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR]:
    os.makedirs(d, exist_ok=True)

# Curated external dataset repository samples for academic fine-tuning & evaluation
DEFAULT_EXTERNAL_DATASET = [
    {
        "id": "ext_kn_001",
        "document": "ಬೆಂಗಳೂರು ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಮಾತ್ರವಲ್ಲದೆ, ಭಾರತದ ಅತ್ಯಂತ ಪ್ರಮುಖ ತಂತ್ರಜ್ಞಾನ ನಗರಿಯಾಗಿದೆ. ಜಾಗತಿಕ ಮಟ್ಟದಲ್ಲಿ ಇದನ್ನು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ. ನೂರಾರು ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ (IT) ಸಂಸ್ಥೆಗಳು, ಉದ್ಯಮಗಳು ಮತ್ತು ನವೋದ್ಯಮಗಳು (Startups) ಇಲ್ಲಿ ತಮ್ಮ ಕೇಂದ್ರ ಕಚೇರಿಗಳನ್ನು ಹೊಂದಿವೆ. ಎಲೆಕ್ಟ್ರಾನಿಕ್ ಸಿಟಿ, ವೈಟ್‌ಫೀಲ್ಡ್, ಮಾನ್ಯತಾ ಟೆಕ್ ಪಾರ್ಕ್ ನಂತಹ ಬೃಹತ್ ತಂತ್ರಜ್ಞಾನ ಪಾರ್ಕ್‌ಗಳು ನಗರದಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿವೆ. ಲಕ್ಷಾಂತರ ಎಂಜಿನಿಯರ್‌ಗಳು, ವಿಜ್ಞಾನಿಗಳು ಮತ್ತು ತಂತ್ರಜ್ಞರು ಬೆಂಗಳೂರಿನಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತಿದ್ದಾರೆ. ಹೊಸ ಆವಿಷ್ಕಾರಗಳು, ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಸಂಶೋಧನೆಯಲ್ಲಿ ಬೆಂಗಳೂರು ಪ್ರಮುಖ ಪಾತ್ರ ವಹಿಸಿದೆ.",
        "summary": "ಬೆಂಗಳೂರು ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಎಂದು ಪ್ರಸಿದ್ಧವಾಗಿದ್ದು, ನೂರಾರು ಐಟಿ ಸಂಸ್ಥೆಗಳು ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಪಾರ್ಕ್‌ಗಳನ್ನು ಹೊಂದಿರುವ ಪ್ರಮುಖ ನವೋದ್ಯಮ ಕೇಂದ್ರವಾಗಿದೆ."
    },
    {
        "id": "ext_kn_002",
        "document": "ಕರ್ನಾಟಕದಲ್ಲಿ ಹರಡಿರುವ ಪಶ್ಚಿಮ ಘಟ್ಟಗಳು ಪ್ರಪಂಚದ ಎಂಟು ಅತ್ಯಂತ ಪ್ರಮುಖ ಜೀವವೈವಿಧ್ಯ ವಲಯಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ. ಇವು ಯುನೆಸ್ಕೋ ವಿಶ್ವ ಪಾರಂಪರಿಕ ತಾಣವೆಂದು ಗುರುತಿಸಲ್ಪಟ್ಟಿವೆ. ಪಶ್ಚಿಮ ಘಟ್ಟಗಳು ದಟ್ಟವಾದ ಕಾಡುಗಳು, ಅಪರೂಪದ ಸಸ್ಯಗಳು, ಪ್ರಾಣಿಗಳು ಮತ್ತು ಪಕ್ಷಿಗಳಿಗೆ ಆಶ್ರಯ ತಾಣವಾಗಿವೆ. ಕಾವೇರಿ, ತುಂಗಭದ್ರಾ, ಶರಾವತಿ ಮತ್ತು ಕಾಳಿ ನದಿಗಳು ಈ ಪರ್ವತ ಶ್ರೇಣಿಯಲ್ಲಿ ಉಗಮಿಸುತ್ತವೆ. ಇವು ದಕ್ಷಿಣ ಭಾರತದ ಕುಡಿಯುವ ನೀರು ಮತ್ತು ಕೃಷಿಗೆ ಪ್ರಮುಖ ಜೀವನಾಡಿಯಾಗಿವೆ. ಆದರೆ, ಅನಿಯಂತ್ರಿತ ಗಣಿಗಾರಿಕೆ ಮತ್ತು ನಗರೀಕರಣದಿಂದ ಪರಿಸರ ಸಮತೋಲನಕ್ಕೆ ಧಕ್ಕೆಯುಂಟಾಗಿದೆ.",
        "summary": "ಯುನೆಸ್ಕೋ ಪಾರಂಪರಿಕ ತಾಣವಾದ ಪಶ್ಚಿಮ ಘಟ್ಟಗಳು ದಕ್ಷಿಣ ಭಾರತದ ಪ್ರಮುಖ ನದಿಗಳ ಉಗಮಸ್ಥಾನವಾಗಿದ್ದು, ಜೀವವೈವಿಧ್ಯದ ಸಂರಕ್ಷಣೆಗೆ ಅತ್ಯಂತ ಪ್ರಮುಖವಾಗಿವೆ."
    },
    {
        "id": "ext_kn_003",
        "document": "ಬಳ್ಳಾರಿ ಜಿಲ್ಲೆಯಲ್ಲಿರುವ ಹಂಪಿ ಯುನೆಸ್ಕೋ ವಿಶ್ವ ಪಾರಂಪರಿಕ ತಾಣವಾಗಿದ್ದು, ವಿಶ್ವಪ್ರಸಿದ್ಧ ಪ್ರವಾಸಿ ಕೇಂದ್ರವಾಗಿದೆ. ಇದು 14ನೇ ಶತಮಾನದ ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯದ ರಾಜಧಾನಿಯಾಗಿತ್ತು. ತುಂಗಭದ್ರಾ ನದಿಯ ದಂಡೆಯಲ್ಲಿರುವ ಹಂಪಿಯಲ್ಲಿ ಅದ್ಭುತ ಕಲ್ಲಿನ ಕೆತ್ತನೆಗಳು, ದೇವಾಲಯಗಳು ಮತ್ತು ಅರಮನೆಗಳ ಅವಶೇಷಗಳನ್ನು ಕಾಣಬಹುದು. ವಿರೂಪಾಕ್ಷ ದೇವಾಲಯ, ವಿಜಯ ವಿಠಲ ದೇವಾಲಯದ ಕಲ್ಲಿನ ರಥ, ಉಗ್ರ ನರಸಿಂಹ ವಿಗ್ರಹ ಮತ್ತು ಕಮಲ ಮಹಲ್ ಇಲ್ಲಿನ ಮುಖ್ಯ ಆಕರ್ಷಣೆಗಳಾಗಿವೆ.",
        "summary": "ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯದ ರಾಜಧಾನಿಯಾಗಿದ್ದ ಹಂಪಿ ಕಲ್ಲಿನ ರಥ ಹಾಗೂ ವಾಸ್ತುಶಿಲ್ಪದ ವೈಭವಕ್ಕೆ ಹೆಸರಾದ ವಿಶ್ವಪ್ರಸಿದ್ಧ ಯುನೆಸ್ಕೋ ಪಾರಂಪರಿಕ ತಾಣವಾಗಿದೆ."
    },
    {
        "id": "ext_kn_004",
        "document": "ಕರ್ನಾಟಕದ ಕೃಷಿ ಕ್ಷೇತ್ರದಲ್ಲಿ ಸಾವಯವ ಕೃಷಿ ಪದ್ಧತಿಗೆ ಆದ್ಯತೆ ಹೆಚ್ಚುತ್ತಿದೆ. ರಾಸಾಯನಿಕ ಗೊಬ್ಬರಗಳು ಮತ್ತು ಕೀಟನಾಶಕಗಳ ಬಳಕೆಯಿಂದ ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಕ್ಷೀಣಿಸುತ್ತಿರುವ ಹಿನ್ನೆಲೆಯಲ್ಲಿ, ರೈತರು ನೈಸರ್ಗಿಕ ಕೃಷಿಯತ್ತ ಮುಖ ಮಾಡುತ್ತಿದ್ದಾರೆ. ಸಾವಯವ ಕೃಷಿಯು ಮಣ್ಣಿನ ಆರೋಗ್ಯವನ್ನು ರಕ್ಷಿಸುವುದಲ್ಲದೆ, ನೈಸರ್ಗಿಕ ತ್ಯಾಜ್ಯಗಳು, ಸಗಣಿ ಗೊಬ್ಬರ ಮತ್ತು ಜೀವಾಮೃತವನ್ನು ಬಳಸುತ್ತದೆ. ಇದರಿಂದ ಬೆಳೆಯುವ ಧಾನ್ಯಗಳು, ತರಕಾರಿಗಳು ಮತ್ತು ಹಣ್ಣುಗಳು ಆರೋಗ್ಯಕರ ಹಾಗೂ ವಿಷಮುಕ್ತವಾಗಿರುತ್ತವೆ.",
        "summary": "ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಉಳಿಸಲು ಕರ್ನಾಟಕದ ರೈತರು ಸಾವಯವ ಕೃಷಿಯತ್ತ ಸಾಗುತ್ತಿದ್ದು, ನೈಸರ್ಗಿಕ ಗೊಬ್ಬರ ಬಳಸಿ ಆರೋಗ್ಯಕರ ವಿಷಮುಕ್ತ ಬೆಳೆ ಬೆಳೆಯುತ್ತಿದ್ದಾರೆ."
    },
    {
        "id": "ext_kn_005",
        "document": "ಭಾರತೀಯ ಬಾಹ್ಯಾಕಾಶ ಸಂಶೋಧನಾ ಸಂಸ್ಥೆ (ISRO) ಜಾಗತಿಕ ಮಟ್ಟದಲ್ಲಿ ಭಾರತದ ಕೀರ್ತಿಯನ್ನು ಎತ್ತಿಹಿಡಿದಿದೆ. ಬೆಂಗಳೂರಿನಲ್ಲಿ ಪ್ರಧಾನ ಕಚೇರಿ ಹೊಂದಿರುವ ಇಸ್ರೋ, ಕಡಿಮೆ ವೆಚ್ಚದಲ್ಲಿ ಯಶಸ್ವಿ ಬಾಹ್ಯಾಕಾಶ ಯೋಜನೆಗಳನ್ನು ಅನುಷ್ಠಾನಗೊಳಿಸಿ ಪ್ರಪಂಚದ ಗಮನ ಸೆಳೆದಿದೆ. ಚಂದ್ರಯಾನ-3 ಯೋಜನೆಯ ಮೂಲಕ ಚಂದ್ರನ ದಕ್ಷಿಣ ಧ್ರುವದಲ್ಲಿ ನೌಕೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಇಳಿಸಿದ ಮೊದಲ ದೇಶ ಎಂಬ ಹೆಗ್ಗಳಿಕೆಗೆ ಭಾರತ ಪಾತ್ರವಾಗಿದೆ. ಮಂಗಳಯಾನ ಮತ್ತು ಆದಿತ್ಯ-L1 ಯೋಜನೆಗಳು ಇಸ್ರೋದ ತಾಂತ್ರಿಕ ಪ್ರಬುದ್ಧತೆಯನ್ನು ತೋರಿಸುತ್ತವೆ.",
        "summary": "ಬೆಂಗಳೂರು ಪ್ರಧಾನ ಕಚೇರಿ ಹೊಂದಿರುವ ಇಸ್ರೋ ಚಂದ್ರಯಾನ-3 ಮತ್ತು ಮಂಗಳಯಾನಗಳ ಮೂಲಕ ಜಾಗತಿಕ ಬಾಹ್ಯಾಕಾಶ ರಂಗದಲ್ಲಿ ಭಾರತದ ಹೆಮ್ಮೆಯ ಸಾಧನೆ ಮಾಡಿದೆ."
    },
    {
        "id": "ext_kn_006",
        "document": "ಕರ್ನಾಟಕ ರಾಜ್ಯವು ಶ್ರೀಮಂತ ಸಾಹಿತ್ಯಿಕ ಪರಂಪರೆಯನ್ನು ಹೊಂದಿದೆ. ಕನ್ನಡ ಭಾಷೆಗೆ ಭಾರತದಲ್ಲಿ ಎಂಟು ಜ್ಞಾನಪೀಠ ಪ್ರಶಸ್ತಿಗಳು ದೊರೆತಿವೆ. ಕುವೆಂಪು, ದ.ರಾ. ಬೇಂದ್ರೆ, ಶಿವರಾಮ ಕಾರಂತ, ಮಾಸ್ತಿ ವೆಂಕಟೇಶ ಅಯ್ಯಂಗಾರ್, ವಿ.ಕೃ. ಗೋಕಾಕ್, ಯು.ಆರ್. ಅನಂತಮೂರ್ತಿ, ಗಿರೀಶ್ ಕಾರ್ನಾಡ್ ಮತ್ತು ಚಂದ್ರಶೇಖರ ಕಂಬಾರ ಅವರುಗಳು ಈ ಗೌರವಕ್ಕೆ ಭಾಜನರಾಗಿದ್ದಾರೆ.",
        "summary": "ಎಂಟು ಜ್ಞಾನಪೀಠ ಪ್ರಶಸ್ತಿಗಳನ್ನು ಪಡೆದಿರುವ ಕನ್ನಡ ಸಾಹಿತ್ಯವು ವಿಶ್ವಪ್ರಸಿದ್ಧ ಕವಿಗಳು ಹಾಗೂ ಮಹೋನ್ನತ ಸಾಹಿತ್ಯಿಕ ಪರಂಪರೆಯನ್ನು ಹೊಂದಿದೆ."
    },
    {
        "id": "ext_kn_007",
        "document": "ಶಿಕ್ಷಣ ರಂಗದಲ್ಲಿ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ಮತ್ತು ಡಿಜಿಟಲ್ ತಂತ್ರಜ್ಞಾನಗಳ ಬಳಕೆ ವೇಗವಾಗಿ ಹೆಚ್ಚುತ್ತಿದೆ. ಆನ್‌ಲೈನ್ ಕಲಿಕಾ ವೇದಿಕೆಗಳು, ವರ್ಚುವಲ್ ತರಗತಿಗಳು ಹಾಗೂ ಇ-ಪುಸ್ತಕಗಳು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸುಲಭವಾಗಿ ಲಭ್ಯವಾಗುತ್ತಿವೆ. ಗ್ರಾಮೀಣ ಪ್ರದೇಶದ ಶಾಲೆಗಳಿಗೂ ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕ ಕಲ್ಪಿಸುವ ಮೂಲಕ ಶಿಕ್ಷಣದ ಗುಣಮಟ್ಟವನ್ನು ಉತ್ತಮಪಡಿಸಲು ಶ್ರಮಿಸಲಾಗುತ್ತಿದೆ.",
        "summary": "ಡಿಜಿಟಲ್ ತಂತ್ರಜ್ಞಾನ ಮತ್ತು ಎಐ ಬಳಕೆಯು ಶಿಕ್ಷಣ ರಂಗದಲ್ಲಿ ಕ್ರಾಂತಿ ಉಂಟುಮಾಡಿದ್ದು, ಆನ್‌ಲೈನ್ ಕಲಿಕೆ ಹಾಗೂ ಇ-ಪುಸ್ತಕಗಳು ಕೌಶಲ್ಯಾಭಿವೃದ್ಧಿಗೆ ನೆರವಾಗುತ್ತಿವೆ."
    },
    {
        "id": "ext_kn_008",
        "document": "ಆರೋಗ್ಯ ಪಾಲನೆಯಲ್ಲಿ ಯೋಗ ಮತ್ತು ಪ್ರಾಣಾಯಾಮಗಳ ಪಾತ್ರ ಅತ್ಯಂತ ಪ್ರಮುಖವಾಗಿದೆ. ಪ್ರತಿದಿನ ಯೋಗಾಭ್ಯಾಸ ಮಾಡುವುದರಿಂದ ಶಾರೀರಿಕ ಮತ್ತು ಮಾನಸಿಕ ಆರೋಗ್ಯ ಉತ್ತಮಗೊಳ್ಳುತ್ತದೆ. ಒತ್ತಡ ನಿಯಂತ್ರಣ, ರೋಗನಿರೋಧಕ ಶಕ್ತಿ ಹೆಚ್ಚಳ ಹಾಗೂ ರಕ್ತಸಂಚಾರ ಸುಧಾರಣೆಗೆ ಯೋಗ ಸಹಕಾರಿಯಾಗಿದೆ.",
        "summary": "ಪ್ರತಿದಿನ ಯೋಗ ಮತ್ತು ಪ್ರಾಣಾಯಾಮ ಮಾಡುವುದರಿಂದ ಒತ್ತಡ ಕಡಿಮೆಯಾಗಿ ಶಾರೀರಿಕ ಹಾಗೂ ಮಾನಸಿಕ ಆರೋಗ್ಯ ವೃದ್ಧಿಸುತ್ತದೆ."
    },
    {
        "id": "ext_kn_009",
        "document": "ಸೌರಶಕ್ತಿ ಮತ್ತು ಪವನಶಕ್ತಿಯಂತಹ ನವೀಕರಿಸಬಹುದಾದ ಇಂಧನ ಮೂಲಗಳಿಗೆ ಕರ್ನಾಟಕ ಸರ್ಕಾರ ಹೆಚ್ಚಿನ ಆದ್ಯತೆ ನೀಡುತ್ತಿದೆ. ತುಮಕೂರು ಜಿಲ್ಲೆಯ ಪಾವಗಡದಲ್ಲಿರುವ ಸೌರಶಕ್ತಿ ಪಾರ್ಕ್ ಪ್ರಪಂಚದ ಅತಿ ದೊಡ್ಡ ಸೌರಶಕ್ತಿ ಯೋಜನೆಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ.",
        "summary": "ಪಾವಗಡದ ಅತಿದೊಡ್ಡ ಸೌರ ಪಾರ್ಕ್ ಒಳಗೊಂಡಂತೆ ಕರ್ನಾಟಕವು ನವೀಕರಿಸಬಹುದಾದ ಹಸಿರು ಇಂಧನ ಉತ್ಪಾದನೆಯಲ್ಲಿ ಮುಂಚೂಣಿಯಲ್ಲಿದೆ."
    },
    {
        "id": "ext_kn_010",
        "document": "ಕರ್ನಾಟಕದ ಮೈಸೂರು ದಸರಾ ಉತ್ಸವವು ಪ್ರಪಂಚದಾದ್ಯಂತ ಪ್ರಸಿದ್ಧವಾಗಿದೆ. 10 ದಿನಗಳ ಕಾಲ ನಡೆಯುವ ಈ ವೈಭವೋಪೇತ ಹಬ್ಬದಲ್ಲಿ ಮೈಸೂರು ಅರಮನೆಯನ್ನು ಲಕ್ಷಾಂತರ ವಿದ್ಯುತ್ ದೀಪಗಳಿಂದ ಅಲಂಕರಿಸಲಾಗುತ್ತದೆ. ಜಂಬೂ ಸವಾರಿ ಪ್ರಮುಖ ಆಕರ್ಷಣೆಯಾಗಿದೆ.",
        "summary": "ಮೈಸೂರು ದಸರಾ 10 ದಿನಗಳ ಸಾಂಸ್ಕೃತಿಕ ವೈಭವದ ಆಚರಣೆಯಾಗಿದ್ದು, ದೀಪಾಲಂಕೃತ ಅರಮನೆ ಹಾಗೂ ಜಂಬೂ ಸವಾರಿಗೆ ಜಾಗತಿಕವಾಗಿ ಪ್ರಸಿದ್ಧವಾಗಿದೆ."
    }
]

def load_external_dataset_from_file(file_path: str) -> List[Dict[str, str]]:
    """Loads external dataset from a local CSV, JSON, or Parquet file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Loading external dataset from file: {file_path}")
    samples = []

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        for idx, row in df.iterrows():
            doc = str(row.get('document', row.get('text', ''))).strip()
            summ = str(row.get('summary', '')).strip()
            if doc and summ:
                samples.append({"id": f"ext_file_{idx}", "document": doc, "summary": summ})
    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for idx, item in enumerate(data):
                doc = str(item.get('document', item.get('text', ''))).strip()
                summ = str(item.get('summary', '')).strip()
                if doc and summ:
                    samples.append({"id": f"ext_file_{idx}", "document": doc, "summary": summ})
    elif file_path.endswith('.parquet'):
        df = pd.read_parquet(file_path)
        for idx, row in df.iterrows():
            doc = str(row.get('document', row.get('text', ''))).strip()
            summ = str(row.get('summary', '')).strip()
            if doc and summ:
                samples.append({"id": f"ext_file_{idx}", "document": doc, "summary": summ})
    
    return samples

def preprocess_and_save_dataset(samples: List[Dict[str, str]], kannada_threshold: float = 0.30):
    print(f"\nPreprocessing {len(samples)} external dataset samples...")
    
    # 1. Save Raw
    raw_path = os.path.join(RAW_DIR, "kannada_raw.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    print(f"Saved raw dataset to: {raw_path}")

    # 2. Clean and Filter
    processed_samples = []
    filtered_count = 0

    for item in samples:
        doc = clean_kannada_text(item["document"])
        summ = clean_kannada_text(item["summary"])
        
        ratio = calculate_kannada_ratio(doc)
        if ratio >= kannada_threshold and len(doc) >= 40 and len(summ) >= 10:
            processed_samples.append({
                "id": item["id"],
                "document": doc,
                "summary": summ,
                "doc_char_len": len(doc),
                "summary_char_len": len(summ),
                "kannada_ratio": round(ratio, 4),
                "language": "kn"
            })
        else:
            filtered_count += 1

    print(f"Cleaned and retained {len(processed_samples)} valid samples (Filtered out {filtered_count} noisy entries).")

    processed_json = os.path.join(PROCESSED_DIR, "kannada_processed.json")
    processed_csv = os.path.join(PROCESSED_DIR, "kannada_processed.csv")
    with open(processed_json, "w", encoding="utf-8") as f:
        json.dump(processed_samples, f, ensure_ascii=False, indent=2)
    pd.DataFrame(processed_samples).to_csv(processed_csv, index=False, encoding="utf-8")

    # 3. 80% Train / 10% Validation / 10% Test Split
    total = len(processed_samples)
    train_end = int(0.8 * total)
    val_end = train_end + int(0.1 * total)

    train_data = processed_samples[:train_end]
    val_data = processed_samples[train_end:val_end]
    test_data = processed_samples[val_end:]

    # Ensure splits are non-empty
    if len(test_data) == 0 and total >= 2:
        test_data = processed_samples[-2:]
        val_data = processed_samples[-3:-2] if total >= 3 else processed_samples[:1]
        train_data = processed_samples[:-3] if total >= 3 else processed_samples[:1]

    print("\nSaving 80-10-10 External Dataset Splits:")
    for name, data, target_dir in [
        ("train", train_data, TRAIN_DIR),
        ("val", val_data, VAL_DIR),
        ("test", test_data, TEST_DIR)
    ]:
        json_file = os.path.join(target_dir, f"kannada_{name}.json")
        csv_file = os.path.join(target_dir, f"kannada_{name}.csv")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        pd.DataFrame(data).to_csv(csv_file, index=False, encoding="utf-8")
        print(f" - {name.upper()} split ({len(data)} items) saved to {target_dir}")

    print("\nExternal dataset preparation completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess external dataset for KannadaSaar")
    parser.add_argument("--file", type=str, help="Path to custom external CSV, JSON, or Parquet dataset file")
    args = parser.parse_args()

    external_samples = []
    if args.file:
        external_samples = load_external_dataset_from_file(args.file)
    else:
        external_samples = DEFAULT_EXTERNAL_DATASET

    preprocess_and_save_dataset(external_samples)
