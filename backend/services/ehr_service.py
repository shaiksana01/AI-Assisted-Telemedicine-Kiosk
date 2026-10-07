"""
Electronic Health Record (EHR) Service for AI-Assisted Telemedicine Kiosk.
Provides longitudinal patient record aggregation and clinical trajectory summaries.
"""

from typing import Dict, Any, List, Optional
import database.database as db

def get_complete_patient_history(patient_id: str) -> Dict[str, Any]:
    """
    Fetch comprehensive EHR history for a given patient ID.
    Includes demographics, all consultations, triage summaries, and prescriptions.
    """
    return db.get_patient_ehr(patient_id)
