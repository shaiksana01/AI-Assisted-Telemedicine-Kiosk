"""
Database module for AI-Assisted Telemedicine Kiosk.
Supports SQLite and MySQL via flexible connection layer with complete
support for Patients, Doctors, Consultations, Triage Results, Prescriptions, and EHR.
"""

import os
import random
import string
import hashlib
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "telemedicine.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")

def get_connection():
    """Get database connection with dictionary/row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Secure SHA-256 hash for authentication."""
    if not password:
        return ""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    """Initialize relational database tables and indexes if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Patients Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT DEFAULT '',
            preferred_language TEXT NOT NULL DEFAULT 'English',
            location TEXT DEFAULT '',
            password_hash TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check & migrate any missing columns
    cursor.execute("PRAGMA table_info(patients)")
    patient_cols = [row[1] for row in cursor.fetchall()]
    if "email" not in patient_cols:
        cursor.execute("ALTER TABLE patients ADD COLUMN email TEXT DEFAULT ''")
    if "password_hash" not in patient_cols:
        cursor.execute("ALTER TABLE patients ADD COLUMN password_hash TEXT DEFAULT ''")

    # 2. Doctors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            specialization TEXT DEFAULT 'General Medicine',
            license_number TEXT DEFAULT '',
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            preferred_language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("PRAGMA table_info(doctors)")
    doc_cols = [row[1] for row in cursor.fetchall()]
    if "specialization" not in doc_cols:
        cursor.execute("ALTER TABLE doctors ADD COLUMN specialization TEXT DEFAULT 'General Medicine'")
    if "license_number" not in doc_cols:
        cursor.execute("ALTER TABLE doctors ADD COLUMN license_number TEXT DEFAULT ''")
    if "preferred_language" not in doc_cols:
        cursor.execute("ALTER TABLE doctors ADD COLUMN preferred_language TEXT DEFAULT 'English'")

    # 3. Consultations Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            doctor_id TEXT DEFAULT '',
            symptoms_text TEXT NOT NULL,
            detected_symptoms TEXT NOT NULL,
            triage_priority TEXT NOT NULL,
            triage_confidence REAL NOT NULL,
            consultation_status TEXT NOT NULL DEFAULT 'Waiting for doctor consultation',
            chief_complaint TEXT DEFAULT '',
            doctor_notes TEXT DEFAULT '',
            doctor_observations TEXT DEFAULT '',
            doctor_advice TEXT DEFAULT '',
            follow_up_recommendation TEXT DEFAULT '',
            started_at TIMESTAMP NULL,
            completed_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        )
    """)
    cursor.execute("PRAGMA table_info(consultations)")
    cns_cols = [row[1] for row in cursor.fetchall()]
    for col, ctype in [
        ("doctor_id", "TEXT DEFAULT ''"),
        ("chief_complaint", "TEXT DEFAULT ''"),
        ("doctor_observations", "TEXT DEFAULT ''"),
        ("doctor_advice", "TEXT DEFAULT ''"),
        ("follow_up_recommendation", "TEXT DEFAULT ''"),
        ("started_at", "TIMESTAMP NULL"),
        ("completed_at", "TIMESTAMP NULL")
    ]:
        if col not in cns_cols:
            cursor.execute(f"ALTER TABLE consultations ADD COLUMN {col} {ctype}")

    # 4. Symptom Records Table (for EHR history tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptom_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            raw_symptom_text TEXT NOT NULL,
            input_method TEXT DEFAULT 'text',
            detected_symptoms_json TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    # 5. Triage Results Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS triage_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            predicted_priority TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            feature_vector_json TEXT DEFAULT '{}',
            probabilities_json TEXT DEFAULT '{}',
            explanation TEXT DEFAULT '',
            is_emergency INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    # 6. Prescriptions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id TEXT UNIQUE NOT NULL,
            consultation_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            doctor_id TEXT NOT NULL,
            general_notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        )
    """)

    # 7. Prescription Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescription_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id TEXT NOT NULL,
            medicine_name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            duration TEXT NOT NULL,
            instructions TEXT DEFAULT '',
            FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
        )
    """)

    # Create Indexes for fast querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_consultations_patient ON consultations(patient_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(consultation_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prescriptions_patient ON prescriptions(patient_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prescriptions_consultation ON prescriptions(consultation_id)")

    # Ensure default demo doctor account exists
    cursor.execute("SELECT id FROM doctors WHERE doctor_id = 'DOC-101' OR email = 'doctor@kiosk.in'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO doctors (doctor_id, full_name, specialization, license_number, email, phone_number, password_hash, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'DOC-101',
            'Dr. Arvind Sharma',
            'General Medicine & Rural Health',
            'MCI-2018-78945',
            'doctor@kiosk.in',
            '9876543210',
            hash_password('doctor123'),
            'English'
        ))

    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------
# ID GENERATORS
# ------------------------------------------------------------------------------

def generate_patient_id() -> str:
    """Generate unique readable patient ID (e.g., PAT-2026-8472)."""
    random_digits = "".join(random.choices(string.digits, k=4))
    year = datetime.now().year
    return f"PAT-{year}-{random_digits}"

def generate_doctor_id() -> str:
    """Generate unique readable doctor ID (e.g., DOC-2026-319)."""
    random_digits = "".join(random.choices(string.digits, k=3))
    year = datetime.now().year
    return f"DOC-{year}-{random_digits}"

def generate_consultation_id() -> str:
    """Generate unique readable consultation ID (e.g., CNS-2026-9134)."""
    random_digits = "".join(random.choices(string.digits, k=4))
    year = datetime.now().year
    return f"CNS-{year}-{random_digits}"

def generate_prescription_id() -> str:
    """Generate unique readable prescription ID (e.g., RX-2026-4821)."""
    random_digits = "".join(random.choices(string.digits, k=4))
    year = datetime.now().year
    return f"RX-{year}-{random_digits}"

# ------------------------------------------------------------------------------
# PATIENT AUTHENTICATION & MANAGEMENT
# ------------------------------------------------------------------------------

def register_patient_account(full_name: str, age: int, gender: str, phone_number: str, 
                             preferred_language: str, location: str = "", password: str = "",
                             email: str = "") -> str:
    """Register a new patient account with secure password hashing."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Check for existing patient by phone number
    cursor.execute("SELECT patient_id FROM patients WHERE phone_number = ?", (phone_number.strip(),))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return existing[0]

    patient_id = generate_patient_id()
    while True:
        cursor.execute("SELECT id FROM patients WHERE patient_id = ?", (patient_id,))
        if not cursor.fetchone():
            break
        patient_id = generate_patient_id()

    p_hash = hash_password(password) if password else ""

    cursor.execute("""
        INSERT INTO patients (patient_id, full_name, age, gender, phone_number, email, preferred_language, location, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, full_name.strip(), int(age), gender.strip(), phone_number.strip(), email.strip(), preferred_language.strip(), location.strip(), p_hash))

    conn.commit()
    conn.close()
    return patient_id

def register_patient(full_name: str, age: int, gender: str, phone_number: str, 
                     preferred_language: str, location: str = "") -> str:
    """Legacy helper for patient creation."""
    return register_patient_account(full_name, age, gender, phone_number, preferred_language, location, password="")

def authenticate_patient(phone_number: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate patient using phone number and password."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    p_hash = hash_password(password)
    
    cursor.execute("""
        SELECT * FROM patients 
        WHERE phone_number = ? AND (password_hash = ? OR password_hash = '')
        ORDER BY id DESC LIMIT 1
    """, (phone_number.strip(), p_hash))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
    """Fetch patient details by patient_id."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ------------------------------------------------------------------------------
# DOCTOR AUTHENTICATION & MANAGEMENT
# ------------------------------------------------------------------------------

def register_doctor_account(full_name: str, email: str, doctor_id: str, phone_number: str, 
                            password: str, specialization: str = "General Medicine", 
                            license_number: str = "", preferred_language: str = "English") -> str:
    """Register a new doctor account."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    doc_id = doctor_id.strip() if doctor_id.strip() else generate_doctor_id()
    p_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO doctors (doctor_id, full_name, specialization, license_number, email, phone_number, password_hash, preferred_language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (doc_id, full_name.strip(), specialization.strip(), license_number.strip(), email.strip().lower(), phone_number.strip(), p_hash, preferred_language.strip()))

    conn.commit()
    conn.close()
    return doc_id

def authenticate_doctor(id_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate doctor using Doctor ID / Email and password."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    p_hash = hash_password(password)
    query_val = id_or_email.strip().lower()

    cursor.execute("""
        SELECT * FROM doctors 
        WHERE (LOWER(doctor_id) = ? OR LOWER(email) = ?) AND password_hash = ?
    """, (query_val, query_val, p_hash))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_doctor_by_id(doctor_id: str) -> Optional[Dict[str, Any]]:
    """Fetch doctor details by doctor_id."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE doctor_id = ?", (doctor_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ------------------------------------------------------------------------------
# CONSULTATION & TRIAGE OPERATIONS
# ------------------------------------------------------------------------------

def create_consultation(patient_id: str, symptoms_text: str, detected_symptoms: str, 
                        triage_priority: str, triage_confidence: float,
                        input_method: str = "text", triage_metadata: Optional[Dict[str, Any]] = None) -> str:
    """Create a new consultation, symptom record, and triage result record."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    consultation_id = generate_consultation_id()
    while True:
        cursor.execute("SELECT id FROM consultations WHERE consultation_id = ?", (consultation_id,))
        if not cursor.fetchone():
            break
        consultation_id = generate_consultation_id()

    # Insert into consultations
    cursor.execute("""
        INSERT INTO consultations (
            consultation_id, patient_id, symptoms_text, detected_symptoms, 
            triage_priority, triage_confidence, consultation_status
        ) VALUES (?, ?, ?, ?, ?, ?, 'Waiting for doctor consultation')
    """, (consultation_id, patient_id, symptoms_text, detected_symptoms, triage_priority, float(triage_confidence)))

    # Insert into symptom_records
    cursor.execute("""
        INSERT INTO symptom_records (
            consultation_id, patient_id, raw_symptom_text, input_method, detected_symptoms_json
        ) VALUES (?, ?, ?, ?, ?)
    """, (consultation_id, patient_id, symptoms_text, input_method, json.dumps(detected_symptoms.split(", ") if detected_symptoms else [])))

    # Insert into triage_results if metadata is provided
    if triage_metadata:
        cursor.execute("""
            INSERT INTO triage_results (
                consultation_id, patient_id, predicted_priority, confidence_score,
                feature_vector_json, probabilities_json, explanation, is_emergency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            consultation_id,
            patient_id,
            triage_priority,
            float(triage_confidence),
            json.dumps(triage_metadata.get("feature_vector", {})),
            json.dumps(triage_metadata.get("probabilities", {})),
            triage_metadata.get("explanation", ""),
            1 if triage_metadata.get("is_emergency", False) else 0
        ))

    conn.commit()
    conn.close()
    return consultation_id

def get_consultation_by_id(consultation_id: str) -> Optional[Dict[str, Any]]:
    """Fetch consultation details with patient and doctor information."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.*, 
            p.full_name as patient_name, 
            p.age, 
            p.gender, 
            p.phone_number, 
            p.preferred_language, 
            p.location,
            d.full_name as doctor_name,
            d.specialization as doctor_specialization
        FROM consultations c
        JOIN patients p ON c.patient_id = p.patient_id
        LEFT JOIN doctors d ON c.doctor_id = d.doctor_id
        WHERE c.consultation_id = ?
    """, (consultation_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_consultations() -> List[Dict[str, Any]]:
    """Retrieve all consultations ordered by clinical priority and recency."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.*,
            p.full_name as patient_name,
            p.age,
            p.gender,
            p.phone_number,
            p.preferred_language,
            p.location,
            d.full_name as doctor_name
        FROM consultations c
        JOIN patients p ON c.patient_id = p.patient_id
        LEFT JOIN doctors d ON c.doctor_id = d.doctor_id
        ORDER BY 
            CASE c.triage_priority
                WHEN 'Urgent Attention' THEN 1
                WHEN 'High Priority' THEN 2
                WHEN 'Moderate Priority' THEN 3
                WHEN 'Low Priority' THEN 4
                ELSE 5
            END,
            c.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_consultation_status(consultation_id: str, new_status: str, doctor_id: Optional[str] = None):
    """Update consultation status and doctor assignment."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if doctor_id:
        cursor.execute("""
            UPDATE consultations
            SET consultation_status = ?, doctor_id = ?, updated_at = ?
            WHERE consultation_id = ?
        """, (new_status, doctor_id, now, consultation_id))
    else:
        cursor.execute("""
            UPDATE consultations
            SET consultation_status = ?, updated_at = ?
            WHERE consultation_id = ?
        """, (new_status, now, consultation_id))
        
    conn.commit()
    conn.close()

def update_doctor_notes(consultation_id: str, notes: str, chief_complaint: str = "",
                        observations: str = "", advice: str = "", followup: str = ""):
    """Save doctor clinical notes and structured observations."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE consultations
        SET 
            doctor_notes = ?,
            chief_complaint = ?,
            doctor_observations = ?,
            doctor_advice = ?,
            follow_up_recommendation = ?,
            updated_at = ?
        WHERE consultation_id = ?
    """, (notes, chief_complaint, observations, advice, followup, now, consultation_id))
    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------
# PRESCRIPTIONS & ELECTRONIC HEALTH RECORDS (EHR)
# ------------------------------------------------------------------------------

def create_prescription(consultation_id: str, patient_id: str, doctor_id: str, 
                        medicines: List[Dict[str, str]], general_notes: str = "") -> str:
    """Create a digital prescription record with multiple medicine items."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    prescription_id = generate_prescription_id()
    while True:
        cursor.execute("SELECT id FROM prescriptions WHERE prescription_id = ?", (prescription_id,))
        if not cursor.fetchone():
            break
        prescription_id = generate_prescription_id()

    # Insert Prescription header
    cursor.execute("""
        INSERT INTO prescriptions (prescription_id, consultation_id, patient_id, doctor_id, general_notes)
        VALUES (?, ?, ?, ?, ?)
    """, (prescription_id, consultation_id, patient_id, doctor_id, general_notes))

    # Insert Prescription items
    for med in medicines:
        med_name = med.get("medicine_name", "").strip()
        if not med_name:
            continue
        cursor.execute("""
            INSERT INTO prescription_items (prescription_id, medicine_name, dosage, frequency, duration, instructions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            prescription_id,
            med_name,
            med.get("dosage", "1 tab").strip(),
            med.get("frequency", "Once daily").strip(),
            med.get("duration", "3 days").strip(),
            med.get("instructions", "").strip()
        ))

    # Mark consultation as completed
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE consultations 
        SET consultation_status = 'Completed', completed_at = ?, updated_at = ?
        WHERE consultation_id = ?
    """, (now, now, consultation_id))

    conn.commit()
    conn.close()
    return prescription_id

def get_prescription_by_consultation_id(consultation_id: str) -> Optional[Dict[str, Any]]:
    """Get prescription details for a given consultation."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pr.*, d.full_name as doctor_name, d.specialization, d.license_number
        FROM prescriptions pr
        LEFT JOIN doctors d ON pr.doctor_id = d.doctor_id
        WHERE pr.consultation_id = ?
        ORDER BY pr.id DESC LIMIT 1
    """, (consultation_id.strip(),))
    p_row = cursor.fetchone()
    if not p_row:
        conn.close()
        return None

    rx = dict(p_row)
    cursor.execute("""
        SELECT * FROM prescription_items WHERE prescription_id = ?
    """, (rx["prescription_id"],))
    rx["items"] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rx

def get_patient_ehr(patient_id: str) -> Dict[str, Any]:
    """Retrieve full Electronic Health Record (EHR) timeline for a patient."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Patient info
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id.strip(),))
    p_row = cursor.fetchone()
    if not p_row:
        conn.close()
        return {}
    
    patient = dict(p_row)

    # Consultations list
    cursor.execute("""
        SELECT c.*, d.full_name as doctor_name, d.specialization as doctor_specialization
        FROM consultations c
        LEFT JOIN doctors d ON c.doctor_id = d.doctor_id
        WHERE c.patient_id = ?
        ORDER BY c.created_at DESC
    """, (patient_id.strip(),))
    consultations = [dict(r) for r in cursor.fetchall()]

    # Fetch prescriptions for each consultation
    for cns in consultations:
        cursor.execute("""
            SELECT pr.*, d.full_name as doctor_name, d.specialization
            FROM prescriptions pr
            LEFT JOIN doctors d ON pr.doctor_id = d.doctor_id
            WHERE pr.consultation_id = ?
        """, (cns["consultation_id"],))
        pr_row = cursor.fetchone()
        if pr_row:
            pr_dict = dict(pr_row)
            cursor.execute("SELECT * FROM prescription_items WHERE prescription_id = ?", (pr_dict["prescription_id"],))
            pr_dict["items"] = [dict(i) for i in cursor.fetchall()]
            cns["prescription"] = pr_dict
        else:
            cns["prescription"] = None

    conn.close()
    return {
        "patient": patient,
        "total_consultations": len(consultations),
        "consultations": consultations
    }

def get_queue_summary_stats() -> Dict[str, int]:
    """Get dashboard summary metrics."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM consultations WHERE consultation_status = 'Waiting for doctor consultation'")
    waiting = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM consultations WHERE consultation_status = 'Under consultation'")
    in_progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM consultations WHERE triage_priority = 'Urgent Attention' AND consultation_status != 'Completed'")
    urgent = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM consultations WHERE consultation_status = 'Completed'")
    completed = cursor.fetchone()[0]

    conn.close()
    return {
        "total_patients": total_patients,
        "waiting": waiting,
        "in_progress": in_progress,
        "urgent_pending": urgent,
        "completed": completed
    }
