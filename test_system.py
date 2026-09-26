"""
Automated Verification and Testing Suite for AI Telemedicine Kiosk.
Tests database operations, patient & doctor auth, ML triage, and translations.
"""

import os
import sys
import time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import (
    init_db,
    register_patient_account,
    authenticate_patient,
    register_doctor_account,
    authenticate_doctor,
    create_consultation,
    get_patient_by_id,
    get_consultation_by_id,
    get_all_consultations,
    update_consultation_status,
    update_doctor_notes,
    get_queue_summary_stats
)
from ml.predict import predict_triage_priority, extract_symptoms_from_text
from utils.translations import get_text, get_available_languages

def test_multilingual():
    print("--- 1. Testing Multilingual Translations ---")
    langs = get_available_languages()
    assert "English" in langs
    assert "Hindi" in langs
    assert "Kannada" in langs
    assert "Telugu" in langs
    
    for l in langs:
        title = get_text("app_title", l)
        disclaimer = get_text("home_disclaimer", l)
        assert len(title) > 0
        assert len(disclaimer) > 0
        print(f"[{l}] Title: {title}")
    print("✅ Multilingual test passed!\n")

def test_database_and_auth():
    print("--- 2. Testing SQLite Database & Authentication ---")
    init_db()
    
    # 1. Test Patient Registration
    test_phone = f"987{int(time.time()) % 10000000:07d}"
    patient_id = register_patient_account(
        full_name="Sunil Kumar",
        age=32,
        gender="Male",
        phone_number=test_phone,
        preferred_language="Kannada",
        location="Mandya Town",
        password="patientpass123"
    )
    assert patient_id.startswith("PAT-")
    print(f"Registered patient: {patient_id}")
    
    # 2. Test Patient Login
    patient_auth = authenticate_patient(test_phone, "patientpass123")
    assert patient_auth is not None
    assert patient_auth["patient_id"] == patient_id
    assert patient_auth["full_name"] == "Sunil Kumar"
    print(f"Authenticated patient: {patient_auth['full_name']}")
    
    # Test Invalid Login
    invalid_auth = authenticate_patient(test_phone, "wrongpassword")
    assert invalid_auth is None
    print("Handled invalid patient login correctly.")
    
    # 3. Test Doctor Registration
    test_doc_id = f"DOC-{int(time.time()) % 10000}"
    test_email = f"doc_{int(time.time())}@telemedicine.in"
    doc_id = register_doctor_account(
        full_name="Dr. Radhika Rao",
        email=test_email,
        doctor_id=test_doc_id,
        phone_number="9876500002",
        password="doctorpass123"
    )
    assert doc_id == test_doc_id
    print(f"Registered doctor: {doc_id}")
    
    # 4. Test Doctor Login by ID and by Email
    doc_auth_by_id = authenticate_doctor(test_doc_id, "doctorpass123")
    assert doc_auth_by_id is not None
    assert doc_auth_by_id["doctor_id"] == test_doc_id
    print(f"Authenticated doctor by ID: {doc_auth_by_id['full_name']}")
    
    doc_auth_by_email = authenticate_doctor(test_email, "doctorpass123")
    assert doc_auth_by_email is not None
    assert doc_auth_by_email["doctor_id"] == test_doc_id
    print(f"Authenticated doctor by Email: {doc_auth_by_email['full_name']}")
    
    # 5. Test Consultation Record Creation
    cid = create_consultation(
        patient_id=patient_id,
        symptoms_text="Severe headache and high fever",
        detected_symptoms="Headache, Fever, High Fever",
        triage_priority="High Priority",
        triage_confidence=0.88
    )
    assert cid.startswith("CNS-")
    print(f"Created consultation: {cid}")
    
    # 6. Test Status & Notes Update
    update_consultation_status(cid, "Under consultation")
    cns_updated = get_consultation_by_id(cid)
    assert cns_updated["consultation_status"] == "Under consultation"
    
    update_doctor_notes(cid, "Advised rest, hydration and paracetamol.")
    cns_notes = get_consultation_by_id(cid)
    assert "paracetamol" in cns_notes["doctor_notes"]
    print("Updated consultation status and notes.")
    
    # 7. Test Queue Summary Stats
    stats = get_queue_summary_stats()
    assert stats["total_patients"] >= 1
    print(f"Queue Stats: {stats}")
    print("✅ Database and Auth tests passed!\n")

def test_ml_pipeline():
    print("--- 3. Testing ML Triage Pipeline ---")
    
    # Low Priority
    res_low = predict_triage_priority("I have a slight cold and mild cough since yesterday.")
    print(f"Mild Case -> Priority: {res_low['predicted_priority']}, Confidence: {res_low['confidence_score']}")
    assert res_low["predicted_priority"] in ["Low Priority", "Moderate Priority"]
    
    # Moderate Priority
    res_mod = predict_triage_priority("I have fever and vomiting with stomach pain.")
    print(f"Moderate Case -> Priority: {res_mod['predicted_priority']}, Confidence: {res_mod['confidence_score']}")
    
    # Urgent Emergency Attention
    res_urgent = predict_triage_priority("Patient is having severe chest pain and breathing difficulty!")
    print(f"Urgent Case -> Priority: {res_urgent['predicted_priority']}, Confidence: {res_urgent['confidence_score']}")
    assert res_urgent["predicted_priority"] == "Urgent Attention"
    assert res_urgent["is_emergency"] is True
    
    print("✅ ML pipeline test passed!\n")

def test_app_import():
    print("--- 4. Testing app.py Import and Syntax ---")
    import app
    print("✅ app.py imported without errors!\n")

if __name__ == "__main__":
    print("==========================================")
    print("RUNNING AI TELEMEDICINE KIOSK FULL TESTS")
    print("==========================================\n")
    test_multilingual()
    test_database_and_auth()
    test_ml_pipeline()
    test_app_import()
    print("==========================================")
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("==========================================")
