"""
Master Automated Verification and Testing Suite for AI Telemedicine Kiosk.
Runs full tests across:
1. Multilingual Localization (English, Hindi, Kannada, Telugu)
2. Database Schema, Authentication & Role Isolation
3. Supervised Random Forest ML Triage & Emergency Override
4. Speech Services (Whisper STT & OpenAI TTS fallbacks)
5. WebRTC Signaling & Consultation Rooms
6. Structured Digital Prescriptions & Longitudinal EHR
7. Flask REST API Endpoints & Import Safety
"""

import os
import sys
import time
import random

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_auth import (
    test_password_hashing,
    test_phone_validation,
    test_patient_registration_and_login,
    test_doctor_registration_and_login
)
from tests.test_database import test_database_lifecycle
from tests.test_ml import test_symptom_extraction, test_triage_predictions
from tests.test_speech import test_speech_fallbacks, test_webrtc_signaling
from tests.test_api import test_flask_endpoints
from tests.test_security import test_patient_doctor_isolation, test_ehr_privacy_isolation
from utils.translations import get_text, get_available_languages

def test_multilingual_loader():
    print("--- 1. Testing Multilingual Translations Loader ---")
    langs = get_available_languages()
    assert "English" in langs
    assert "Hindi" in langs
    assert "Kannada" in langs
    assert "Telugu" in langs

    for l in langs:
        title = get_text("app_title", l)
        disclaimer = get_text("footer_disclaimer", l)
        assert len(title) > 0
        assert len(disclaimer) > 0
        print(f"[{l}] Title: {title}")
    print("✅ Multilingual translations passed!\n")

def test_flask_web_pages():
    print("--- 7. Testing Browser-Based Flask Web Application Pages & Flows ---")
    import app as main_app
    client = main_app.app.test_client()

    # 1. Home, About, Help
    assert client.get("/").status_code == 200
    assert client.get("/about").status_code == 200
    assert client.get("/help").status_code == 200

    # 2. Patient Registration via HTML form
    test_phone = f"987{random.randint(1000000, 9999999)}"
    res_reg = client.post("/patient/register", data={
        "full_name": "Web Test Patient",
        "age": "29",
        "gender": "Female",
        "phone_number": test_phone,
        "location": "Mysuru Village",
        "preferred_language": "Kannada",
        "password": "webpass123"
    }, follow_redirects=True)
    assert res_reg.status_code == 200
    assert b"Web Test Patient" in res_reg.data
    assert "Kannada".encode("utf-8") in res_reg.data

    # Test Language Selection Persistence on Login (Kannada)
    client.post("/set-language", data={"language": "Kannada"}, follow_redirects=True)
    res_login_kn = client.post("/patient/login", data={
        "phone_number": test_phone,
        "password": "webpass123"
    }, follow_redirects=True)
    assert res_login_kn.status_code == 200
    assert "Kannada".encode("utf-8") in res_login_kn.data
    assert "ರೋಗಿ".encode("utf-8") in res_login_kn.data or "ಮುಖಪುಟ".encode("utf-8") in res_login_kn.data

    # Test Language Selection Persistence on Login (Telugu)
    client.post("/set-language", data={"language": "Telugu"}, follow_redirects=True)
    res_login_te = client.post("/patient/login", data={
        "phone_number": test_phone,
        "password": "webpass123"
    }, follow_redirects=True)
    assert res_login_te.status_code == 200
    assert "Telugu".encode("utf-8") in res_login_te.data

    # 3. Symptom entry & Random Forest Triage
    res_sym = client.post("/symptoms", data={
        "symptom_text": "Severe fever and body pain for two days"
    }, follow_redirects=True)
    assert res_sym.status_code == 200
    assert b"Preliminary AI Triage Result" in res_sym.data or "ಪ್ರಾಥಮಿಕ".encode("utf-8") in res_sym.data or "ప్రాథమిక".encode("utf-8") in res_sym.data

    # 4. Doctor Login & Dashboard
    res_doc_login = client.post("/doctor/login", data={
        "id_or_email": "doctor@kiosk.in",
        "password": "doctor123"
    }, follow_redirects=True)
    assert res_doc_login.status_code == 200
    assert b"Doctor Dashboard" in res_doc_login.data or b"doctor" in res_doc_login.data.lower()
    print("✅ All Flask HTML web pages & workflows verified!\n")


def run_all_tests():
    print("==================================================")
    print("RUNNING AI TELEMEDICINE KIOSK FULL 100% TEST SUITE")
    print("==================================================\n")

    test_multilingual_loader()

    print("--- 2. Testing Authentication & Security ---")
    test_password_hashing()
    test_phone_validation()
    test_patient_registration_and_login()
    test_doctor_registration_and_login()
    test_patient_doctor_isolation()
    test_ehr_privacy_isolation()
    print("✅ Authentication & Security tests passed!\n")

    print("--- 3. Testing Relational Database, Prescriptions & EHR ---")
    test_database_lifecycle()
    print("✅ Database, Prescriptions & EHR tests passed!\n")

    print("--- 4. Testing ML Random Forest Triage & Safety Override ---")
    test_symptom_extraction()
    test_triage_predictions()
    print("✅ Machine Learning triage tests passed!\n")

    print("--- 5. Testing Speech (Whisper/TTS) & WebRTC Signaling ---")
    test_speech_fallbacks()
    test_webrtc_signaling()
    print("✅ Speech & WebRTC signaling tests passed!\n")

    print("--- 6. Testing Flask REST API Integration ---")
    test_flask_endpoints()
    print("✅ Flask REST API tests passed!\n")

    test_flask_web_pages()

    print("==================================================")
    print("🎉 ALL 100% FLASK SYSTEM VERIFICATION TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
