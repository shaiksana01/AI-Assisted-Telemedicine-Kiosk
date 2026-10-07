"""
Unit Tests for Machine Learning Triage Model.
"""

from ml.predict import predict_triage_priority, extract_symptoms_from_text, load_triage_model

def test_symptom_extraction():
    # Mild cold and cough
    feat, keys = extract_symptoms_from_text("I have a slight cold and coughing since yesterday")
    assert "cold" in keys
    assert "cough" in keys

    # Multilingual Hindi
    feat_hi, keys_hi = extract_symptoms_from_text("Mujhe 2 din se tez bukhar aur sar dard hai")
    assert "high_fever" in keys_hi or "fever" in keys_hi
    assert "headache" in keys_hi

    # Multilingual Kannada
    feat_kn, keys_kn = extract_symptoms_from_text("Nimage talenoavu matte jwara ide")
    assert "headache" in keys_kn
    assert "fever" in keys_kn

def test_triage_predictions():
    # Model load test
    model_payload = load_triage_model()
    assert "model" in model_payload
    assert "feature_names" in model_payload

    # Mild case
    res_mild = predict_triage_priority("I have a mild runny nose and slight sneeze")
    assert res_mild["predicted_priority"] in ["Low Priority", "Moderate Priority"]
    assert res_mild["is_emergency"] is False

    # Emergency safety override
    res_emergency = predict_triage_priority("Severe chest pain, breathlessness, patient is collapsing!")
    assert res_emergency["predicted_priority"] == "Urgent Attention"
    assert res_emergency["is_emergency"] is True

    # Unknown symptoms safe handling
    res_unknown = predict_triage_priority("I am feeling a strange unusual sensation in my arm")
    assert res_unknown["predicted_priority"] == "Low Priority"
    assert "General Mild Discomfort" in res_unknown["detected_symptoms"][0]

if __name__ == "__main__":
    test_symptom_extraction()
    test_triage_predictions()
    print("✅ All ML triage tests passed!")
