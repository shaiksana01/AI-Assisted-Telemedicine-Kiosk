"""
Security & Role-Based Authorization Tests.
"""

import time
import database.database as db
from backend.services.ehr_service import get_complete_patient_history

def test_patient_doctor_isolation():
    # 1. Verify Patient cannot authenticate with doctor credentials
    test_phone = f"987{int(time.time() + 30) % 10000000:07d}"
    pid = db.register_patient_account(
        full_name="Patient Private",
        age=30,
        gender="Female",
        phone_number=test_phone,
        preferred_language="English",
        password="patientonlypassword"
    )

    # Doctor auth should fail with patient credentials
    doc_attempt = db.authenticate_doctor(test_phone, "patientonlypassword")
    assert doc_attempt is None

    # Patient auth should fail with doctor credentials
    pat_attempt = db.authenticate_patient("9876543210", "doctor123")
    # Patient with doctor's number does not exist
    assert pat_attempt is None or pat_attempt["full_name"] != "Dr. Arvind Sharma"

def test_ehr_privacy_isolation():
    # Create two separate patients
    phone_a = f"987{int(time.time() + 40) % 10000000:07d}"
    phone_b = f"987{int(time.time() + 50) % 10000000:07d}"
    
    pid_a = db.register_patient_account("Patient Alpha", 40, "Male", phone_a, "English", password="pwdA")
    pid_b = db.register_patient_account("Patient Beta", 35, "Female", phone_b, "English", password="pwdB")

    # Create consultation for Alpha
    cid_a = db.create_consultation(pid_a, "Alpha symptoms", "Fever", "Low Priority", 0.9)

    # Create consultation for Beta
    cid_b = db.create_consultation(pid_b, "Beta symptoms", "Headache", "Moderate Priority", 0.85)

    # Fetch EHR for Alpha
    ehr_a = get_complete_patient_history(pid_a)
    c_ids_a = [c["consultation_id"] for c in ehr_a["consultations"]]

    # Fetch EHR for Beta
    ehr_b = get_complete_patient_history(pid_b)
    c_ids_b = [c["consultation_id"] for c in ehr_b["consultations"]]

    # Verify complete isolation: Alpha's consultations are NOT in Beta's EHR and vice-versa
    assert cid_a in c_ids_a
    assert cid_a not in c_ids_b
    assert cid_b in c_ids_b
    assert cid_b not in c_ids_a

if __name__ == "__main__":
    test_patient_doctor_isolation()
    test_ehr_privacy_isolation()
    print("✅ All security and authorization isolation tests passed!")
