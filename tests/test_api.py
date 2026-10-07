"""
Integration Tests for Flask REST API Endpoints.
"""

import json
import time
from backend.app import create_app

def test_flask_endpoints():
    app = create_app()
    client = app.test_client()

    # 1. Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json["status"] == "healthy"

    # 2. Patient registration via API
    test_phone = f"987{int(time.time() + 20) % 10000000:07d}"
    res_reg = client.post("/api/auth/patient/register", json={
        "full_name": "API Test Patient",
        "age": 34,
        "gender": "Male",
        "phone_number": test_phone,
        "preferred_language": "English",
        "password": "apipassword123"
    })
    assert res_reg.status_code == 201
    patient_id = res_reg.json["patient_id"]

    # 3. Patient login via API
    res_login = client.post("/api/auth/patient/login", json={
        "phone_number": test_phone,
        "password": "apipassword123"
    })
    assert res_login.status_code == 200
    assert res_login.json["patient"]["patient_id"] == patient_id

    # 4. Triage prediction endpoint
    res_triage = client.post("/api/triage/predict", json={
        "symptoms_text": "I have fever and severe headache for two days",
        "additional_symptoms": ["fever", "headache"]
    })
    assert res_triage.status_code == 200
    triage_info = res_triage.json["triage"]
    assert "predicted_priority" in triage_info

    # 5. Create consultation via API
    res_cns = client.post("/api/consultations", json={
        "patient_id": patient_id,
        "symptoms_text": "I have fever and severe headache for two days",
        "detected_symptoms": "Fever, Headache",
        "triage_priority": triage_info["predicted_priority"],
        "triage_confidence": triage_info["confidence_score"]
    })
    assert res_cns.status_code == 201
    consultation_id = res_cns.json["consultation_id"]

    # 6. Doctor issue prescription via API
    res_rx = client.post("/api/prescriptions", json={
        "consultation_id": consultation_id,
        "patient_id": patient_id,
        "doctor_id": "DOC-101",
        "medicines": [
            {"medicine_name": "Paracetamol 500mg", "dosage": "1 tab", "frequency": "Twice daily", "duration": "3 days", "instructions": "After food"}
        ],
        "general_notes": "Advised rest and fluid intake."
    })
    assert res_rx.status_code == 201
    assert "prescription_id" in res_rx.json

    # 7. Get EHR via API
    res_ehr = client.get(f"/api/patients/{patient_id}/ehr")
    assert res_ehr.status_code == 200
    assert res_ehr.json["ehr"]["total_consultations"] >= 1

    # 8. WebRTC Room Signaling API
    res_join = client.post(f"/api/webrtc/room/{consultation_id}/join", json={
        "role": "patient",
        "user_id": patient_id
    })
    assert res_join.status_code == 200

if __name__ == "__main__":
    test_flask_endpoints()
    print("✅ All Flask REST API tests passed!")
