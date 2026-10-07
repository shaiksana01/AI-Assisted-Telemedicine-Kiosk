"""
Unit Tests for Database Operations, Prescriptions, and EHR.
"""

import time
import database.database as db
from backend.services.ehr_service import get_complete_patient_history

def test_database_lifecycle():
    db.init_db()

    # 1. Register Patient
    test_phone = f"987{int(time.time() + 10) % 10000000:07d}"
    pid = db.register_patient_account(
        full_name="Anand Kumar",
        age=45,
        gender="Male",
        phone_number=test_phone,
        preferred_language="Telugu",
        location="Guntur",
        password="anandpass123"
    )
    assert pid.startswith("PAT-")

    # 2. Create Consultation
    cid = db.create_consultation(
        patient_id=pid,
        symptoms_text="Fever, shivering and body ache for 2 days",
        detected_symptoms="Fever, Body Pain",
        triage_priority="Moderate Priority",
        triage_confidence=0.89,
        input_method="text"
    )
    assert cid.startswith("CNS-")

    # 3. Doctor Update Status & Notes
    db.update_consultation_status(cid, "Under consultation", doctor_id="DOC-101")
    cns = db.get_consultation_by_id(cid)
    assert cns["consultation_status"] == "Under consultation"
    assert cns["doctor_id"] == "DOC-101"

    db.update_doctor_notes(
        consultation_id=cid,
        notes="Viral fever suspected. Prescribed antipyretics.",
        chief_complaint="Fever and chills",
        observations="Temperature 100.4F, throat clear",
        advice="Take rest and drink plenty of fluids",
        followup="Re-examine if fever exceeds 3 days"
    )

    # 4. Create Prescription
    medicines = [
        {"medicine_name": "Paracetamol 650mg", "dosage": "1 tab", "frequency": "Thrice daily", "duration": "3 days", "instructions": "After food"},
        {"medicine_name": "Vitamin C 500mg", "dosage": "1 tab", "frequency": "Once daily", "duration": "5 days", "instructions": "Morning"}
    ]
    rx_id = db.create_prescription(
        consultation_id=cid,
        patient_id=pid,
        doctor_id="DOC-101",
        medicines=medicines,
        general_notes="Rest & Hydration"
    )
    assert rx_id.startswith("RX-")

    # 5. Verify EHR History
    ehr = get_complete_patient_history(pid)
    assert ehr["patient"]["patient_id"] == pid
    assert ehr["total_consultations"] >= 1
    latest_cns = ehr["consultations"][0]
    assert latest_cns["consultation_id"] == cid
    assert latest_cns["consultation_status"] == "Completed"
    assert latest_cns["prescription"] is not None
    assert len(latest_cns["prescription"]["items"]) == 2

if __name__ == "__main__":
    test_database_lifecycle()
    print("✅ All database & EHR tests passed!")
