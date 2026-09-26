"""
Inference and Symptom Processing Pipeline for AI-Assisted Telemedicine Kiosk.
Extracts clinical symptom features from free-text using multilingual NLP keyword mapping
and generates preliminary triage predictions via the trained Random Forest model.
"""

import os
import re
import joblib
from typing import Dict, List, Tuple, Any

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "triage_model.pkl")

SYMPTOM_COLUMNS = [
    "fever",
    "cough",
    "cold",
    "headache",
    "body_pain",
    "fatigue",
    "sore_throat",
    "vomiting",
    "diarrhea",
    "abdominal_pain",
    "dizziness",
    "chest_pain",
    "breathing_difficulty",
    "high_fever",
    "loss_of_consciousness",
    "severe_bleeding"
]

# Multilingual and clinical keyword mapping
SYMPTOM_KEYWORDS = {
    "high_fever": [
        "high fever", "burning fever", "102", "103", "104", "tez bukhar", "bada bukhar", 
        "teevra jwara", "atheevra jwara", "theevra jwaram", "high temperature"
    ],
    "fever": [
        "fever", "temperature", "chills", "shivering", "bukhar", "tapam", "taap", 
        "jwara", "jvara", "jwaram", "feverish"
    ],
    "cough": [
        "cough", "coughing", "khasi", "khansi", "kemmu", "khemmu", "daggu", "daggutundi", 
        "dry cough", "wet cough", "phlegm"
    ],
    "cold": [
        "cold", "runny nose", "running nose", "blocked nose", "sneezing", "sardi", 
        "jukaam", "nazla", "sheetala", "jaladosha", "jalubu", "nasal congestion"
    ],
    "headache": [
        "headache", "head pain", "migraine", "sar dard", "sar me dard", "shirovyathe", 
        "talenoavu", "tale novu", "thala noppi", "tala noppi", "head throbbing"
    ],
    "body_pain": [
        "body pain", "body ache", "muscle pain", "joint pain", "badan dard", "jism dard", 
        "mai noavu", "mai kaim noavu", "ollu noppulu", "mey noppi", "bodyaches", "myalgia"
    ],
    "fatigue": [
        "fatigue", "weakness", "weak", "exhausted", "exhaustion", "lethargy", "kamzori", 
        "thakan", "alasate", "neersam", "neerasam", "alasata", "tired"
    ],
    "sore_throat": [
        "sore throat", "throat pain", "throat irritation", "difficulty swallowing", 
        "gale me dard", "gala kharab", "gantu novu", "gonthu noppi", "throat infection"
    ],
    "vomiting": [
        "vomiting", "vomit", "nausea", "throwing up", "puking", "ulti", "oekathisu", 
        "vanthi", "vaanti", "vomitting"
    ],
    "diarrhea": [
        "diarrhea", "loose motion", "loose motions", "stomach upset", "watery stool", 
        "dast", "pet kharab", "bedi", "jhedalu", "motions"
    ],
    "abdominal_pain": [
        "stomach pain", "abdominal pain", "belly pain", "stomach ache", "cramp", 
        "pet dard", "potte novu", "hotte novu", "kadupu noppi", "gastric pain"
    ],
    "dizziness": [
        "dizziness", "dizzy", "vertigo", "giddiness", "lightheaded", "chakkar", 
        "sar ghoomna", "thale suthu", "thala thirugudu", "talatippadam"
    ],
    "chest_pain": [
        "chest pain", "chest tightness", "heart pain", "angina", "chest pressure", 
        "chhati dard", "seene me dard", "edeya novu", "gunde noppi", "chaathi noppi"
    ],
    "breathing_difficulty": [
        "breathing difficulty", "shortness of breath", "breathless", "breathlessness", 
        "asthma", "wheezing", "saans lene me dikkat", "saans phoolna", "usirata samasye", 
        "oopiri aadtledu", "oopiri aadaka", "struggling to breathe"
    ],
    "loss_of_consciousness": [
        "unconscious", "blackout", "collapsed", "passed out", "fainted", "fainting", 
        "behosh", "behoshi", "spruhe thappu", "telivi thappadam", "loss of consciousness"
    ],
    "severe_bleeding": [
        "severe bleeding", "heavy bleeding", "blood loss", "profuse bleeding", 
        "khoon bahna", "raktha srava", "rakta", "nethuru karadam", "haemorrhage"
    ]
}

# Human friendly display labels
SYMPTOM_DISPLAY_NAMES = {
    "fever": "Fever / बुखार / ಜ್ವರ / జ్వరం",
    "high_fever": "High Fever (102°F+) / तेज बुखार / ತೀವ್ರ ಜ್ವರ / తీవ్ర జ్వరం",
    "cough": "Cough / खांसी / ಕೆಮ್ಮು / దగ్గు",
    "cold": "Cold & Congestion / सर्दी / ಶೀತ / జలుబు",
    "headache": "Headache / सिरदर्द / ತಲೆನೋವು / తలనొప్పి",
    "body_pain": "Body Pain / बदन दर्द / ಮೈಕೈ ನೋವು / ఒళ్లు నొప్పులు",
    "fatigue": "Weakness & Fatigue / थकान व कमजोरी / ನಿಶ್ಯಕ್ತಿ / అలసట & నీరసం",
    "sore_throat": "Sore Throat / गले में खराश / ಗಂಟಲು ನೋವು / గొంతు నొప్పి",
    "vomiting": "Vomiting / Nausea / उल्टी / ವಾಂತಿ / వాంతులు",
    "diarrhea": "Diarrhea / Loose Motions / दस्त / ಭೇದಿ / విరేచనాలు",
    "abdominal_pain": "Abdominal Pain / पेट दर्द / ಹೊಟ್ಟೆ ನೋವು / కడుపు నొప్పి",
    "dizziness": "Dizziness / चक्कर / ತಲೆಸುತ್ತು / కళ్ళు తిరగడం",
    "chest_pain": "Chest Pain / छाती में दर्द / ಎದೆ ನೋವು / ఛాతీ నొప్పి",
    "breathing_difficulty": "Difficulty Breathing / सांस लेने में तकलीफ / ಉಸಿರಾಟದ ತೊಂದರೆ / శ్వాస తీసుకోవడంలో ఇబ్బంది",
    "loss_of_consciousness": "Loss of Consciousness / बेहोशी / ಪ್ರಜ್ಞೆ ತಪ್ಪುವುದು / స్పృహ తప్పడం",
    "severe_bleeding": "Severe Bleeding / भारी रक्तस्राव / ತೀವ್ರ ರಕ್ತಸ್ರಾವ / తీవ్ర రక్తస్రావం"
}

_cached_model = None

def load_triage_model():
    """Load or cache the trained ML model."""
    global _cached_model
    if _cached_model is not None:
        return _cached_model

    if not os.path.exists(MODEL_PATH):
        # Auto-train if model doesn't exist yet
        from ml.train_model import train_and_evaluate
        train_and_evaluate()

    _cached_model = joblib.load(MODEL_PATH)
    return _cached_model

def extract_symptoms_from_text(text: str) -> Tuple[Dict[str, int], List[str]]:
    """
    Parse free-text symptom description and map to binary feature representation.
    Returns: (features_dict, list_of_detected_symptom_keys)
    """
    normalized_text = " " + re.sub(r"[^\w\s]", " ", text.lower()) + " "
    features = {col: 0 for col in SYMPTOM_COLUMNS}
    detected_keys = []

    # High fever detection check
    if any(k in normalized_text for k in SYMPTOM_KEYWORDS["high_fever"]):
        features["high_fever"] = 1
        features["fever"] = 1
        detected_keys.append("high_fever")
        detected_keys.append("fever")

    # Match all other keywords
    for symptom, keywords in SYMPTOM_KEYWORDS.items():
        if symptom == "high_fever":
            continue
        for kw in keywords:
            # Word boundary matching or phrase containment
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, normalized_text):
                features[symptom] = 1
                if symptom not in detected_keys:
                    detected_keys.append(symptom)
                break

    return features, detected_keys

def predict_triage_priority(symptom_text: str, additional_selected_symptoms: List[str] = None) -> Dict[str, Any]:
    """
    Run triage prediction on patient symptoms.
    Combines text parsing with any explicitly clicked symptom chips.
    Returns complete structured decision-support metadata.
    """
    model_payload = load_triage_model()
    model = model_payload["model"]
    classes = model_payload["classes"]

    # 1. Extract features from text
    features, detected_keys = extract_symptoms_from_text(symptom_text)

    # 2. Integrate any explicitly clicked helper chips
    if additional_selected_symptoms:
        for sym in additional_selected_symptoms:
            if sym in features:
                features[sym] = 1
                if sym not in detected_keys:
                    detected_keys.append(sym)

    # Convert to feature DataFrame to preserve column names
    import pandas as pd
    feature_vector = [features[col] for col in SYMPTOM_COLUMNS]
    feature_df = pd.DataFrame([feature_vector], columns=SYMPTOM_COLUMNS)

    # Handle edge case when no symptoms could be mapped
    if sum(feature_vector) == 0:
        return {
            "predicted_priority": "Low Priority",
            "confidence_score": 0.85,
            "detected_symptoms": ["General Mild Discomfort (No specific severe markers detected)"],
            "detected_keys": [],
            "feature_vector": features,
            "explanation": "No specific acute or urgent clinical keywords were detected. Classified as Low Priority for general doctor review.",
            "is_emergency": False,
            "probabilities": {cls: (0.85 if cls == "Low Priority" else 0.05) for cls in classes}
        }

    # 3. Model inference
    probabilities = model.predict_proba(feature_df)[0]
    predicted_class = model.predict(feature_df)[0]
    confidence = float(max(probabilities))

    prob_dict = {cls: round(float(prob), 3) for cls, prob in zip(classes, probabilities)}

    # 4. Clinical Safety Override (Rule-based safety layer for red-flag emergencies)
    # Chest pain, breathing difficulty, loss of consciousness, severe bleeding are immediate red flags
    is_emergency = False
    if features.get("loss_of_consciousness") or features.get("severe_bleeding") or (features.get("chest_pain") and features.get("breathing_difficulty")):
        predicted_class = "Urgent Attention"
        confidence = 0.98
        is_emergency = True
        explanation = "Critical emergency markers (e.g., chest pain, respiratory distress, severe bleeding, or loss of consciousness) detected. Immediate priority assigned."
    elif features.get("chest_pain") or features.get("breathing_difficulty"):
        predicted_class = "Urgent Attention"
        confidence = max(confidence, 0.92)
        is_emergency = True
        explanation = "High-risk cardiopulmonary symptoms detected. Escalated to Urgent Attention for expedited medical evaluation."
    elif predicted_class == "Urgent Attention":
        explanation = "Critical severity pattern identified by Random Forest model. Immediate medical triage recommended."
    elif predicted_class == "High Priority":
        explanation = "Combination of acute symptoms (such as high fever with multi-symptom illness) classified as High Priority."
    elif predicted_class == "Moderate Priority":
        explanation = "Moderate symptom cluster identified. Requires prompt clinical assessment."
    else:
        explanation = "Mild or non-acute symptom pattern identified. Suitable for standard consultation queue."

    human_detected = [SYMPTOM_DISPLAY_NAMES.get(k, k.replace("_", " ").title()) for k in detected_keys]

    return {
        "predicted_priority": predicted_class,
        "confidence_score": round(confidence, 2),
        "detected_symptoms": human_detected,
        "detected_keys": detected_keys,
        "feature_vector": features,
        "explanation": explanation,
        "is_emergency": is_emergency,
        "probabilities": prob_dict
    }
