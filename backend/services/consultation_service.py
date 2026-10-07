"""
Consultation Management Service for AI-Assisted Telemedicine Kiosk.
"""

from typing import Dict, Any, List, Optional
import database.database as db

def get_waiting_queue() -> List[Dict[str, Any]]:
    """Retrieve all consultations currently waiting for doctor consultation, prioritized by triage urgency."""
    all_cns = db.get_all_consultations()
    return [c for c in all_cns if c.get("consultation_status") == "Waiting for doctor consultation"]

def get_active_consultations() -> List[Dict[str, Any]]:
    """Retrieve all consultations currently under active doctor review/call."""
    all_cns = db.get_all_consultations()
    return [c for c in all_cns if c.get("consultation_status") == "Under consultation"]

def get_completed_consultations() -> List[Dict[str, Any]]:
    """Retrieve all completed consultation records."""
    all_cns = db.get_all_consultations()
    return [c for c in all_cns if c.get("consultation_status") == "Completed"]
