"""
Authentication and Authorization Service for AI-Assisted Telemedicine Kiosk.
Handles password hashing, token validation, and role-based permissions.
"""

import hashlib
import re
from typing import Dict, Any, Optional, Tuple

def hash_password(password: str) -> str:
    """Generate SHA-256 hash of plaintext password."""
    if not password:
        return ""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password match."""
    return hash_password(plain_password) == hashed_password

def validate_phone_number(phone: str) -> bool:
    """Validate 10-digit Indian mobile number."""
    clean = re.sub(r"[^\d]", "", phone)
    return len(clean) == 10 and clean[0] in "6789"

def validate_patient_registration(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate patient registration inputs."""
    if not data.get("full_name", "").strip():
        return False, "Full name is required."
    try:
        age = int(data.get("age", 0))
        if age <= 0 or age > 125:
            return False, "Please enter a valid age between 1 and 125."
    except (ValueError, TypeError):
        return False, "Age must be a valid number."
    
    gender = data.get("gender", "").strip()
    if not gender or gender.startswith("--"):
        return False, "Please select a valid gender."
    
    phone = data.get("phone_number", "").strip()
    if not validate_phone_number(phone):
        return False, "Please enter a valid 10-digit mobile number."
    
    password = data.get("password", "")
    if password and len(password) < 4:
        return False, "Password must be at least 4 characters long."

    return True, None

def validate_doctor_registration(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate doctor registration inputs."""
    if not data.get("full_name", "").strip():
        return False, "Doctor full name is required."
    email = data.get("email", "").strip()
    if not email or "@" not in email or "." not in email:
        return False, "A valid official email is required."
    phone = data.get("phone_number", "").strip()
    if not phone or len(re.sub(r"[^\d]", "", phone)) < 10:
        return False, "A valid 10-digit phone number is required."
    password = data.get("password", "")
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long."
    return True, None
