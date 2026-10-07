"""
Unit Tests for Authentication and Role-Based Security.
"""

import time
import database.database as db
from backend.auth.auth_service import hash_password, verify_password, validate_phone_number

def test_password_hashing():
    pwd = "securepassword123"
    h1 = hash_password(pwd)
    h2 = hash_password(pwd)
    assert h1 == h2
    assert h1 != pwd
    assert verify_password(pwd, h1) is True
    assert verify_password("wrongpassword", h1) is False

def test_phone_validation():
    assert validate_phone_number("9876543210") is True
    assert validate_phone_number("8888888888") is True
    assert validate_phone_number("12345") is False
    assert validate_phone_number("abcdefghij") is False

def test_patient_registration_and_login():
    test_phone = f"987{int(time.time()) % 10000000:07d}"
    pid = db.register_patient_account(
        full_name="Meena Kumari",
        age=28,
        gender="Female",
        phone_number=test_phone,
        preferred_language="Hindi",
        location="Rampur Village",
        password="patientpass123"
    )
    assert pid.startswith("PAT-")
    
    # Valid login
    auth_patient = db.authenticate_patient(test_phone, "patientpass123")
    assert auth_patient is not None
    assert auth_patient["patient_id"] == pid
    assert auth_patient["full_name"] == "Meena Kumari"

    # Invalid login
    invalid = db.authenticate_patient(test_phone, "wrongpass")
    assert invalid is None

def test_doctor_registration_and_login():
    test_email = f"doc_{int(time.time())}@hospital.in"
    doc_id = db.register_doctor_account(
        full_name="Dr. Suresh Rao",
        email=test_email,
        doctor_id="",
        phone_number="9876543299",
        password="docsecurepass123",
        specialization="Cardiology"
    )
    assert doc_id.startswith("DOC-")

    # Login via Email
    doc_auth = db.authenticate_doctor(test_email, "docsecurepass123")
    assert doc_auth is not None
    assert doc_auth["doctor_id"] == doc_id
    assert doc_auth["specialization"] == "Cardiology"

    # Login via Doctor ID
    doc_auth_id = db.authenticate_doctor(doc_id, "docsecurepass123")
    assert doc_auth_id is not None
    assert doc_auth_id["email"] == test_email

if __name__ == "__main__":
    test_password_hashing()
    test_phone_validation()
    test_patient_registration_and_login()
    test_doctor_registration_and_login()
    print("✅ All auth tests passed!")
