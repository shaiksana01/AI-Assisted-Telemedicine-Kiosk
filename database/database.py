"""
Database module for AI-Assisted Telemedicine Kiosk.
SQLite database storage for patients, doctors, and consultations.
"""

import sqlite3
import os
import random
import string
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "telemedicine.db")

def get_connection():
    """Get SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Simple SHA256 hash for student prototype authentication."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    """Initialize database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Patients Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            preferred_language TEXT NOT NULL DEFAULT 'English',
            location TEXT,
            password_hash TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check and migrate columns if table already existed without password_hash
    cursor.execute("PRAGMA table_info(patients)")
    columns = [row[1] for row in cursor.fetchall()]
    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE patients ADD COLUMN password_hash TEXT DEFAULT ''")

    # Doctors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Consultations Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id TEXT UNIQUE NOT NULL,
            patient_id TEXT NOT NULL,
            symptoms_text TEXT NOT NULL,
            detected_symptoms TEXT NOT NULL,
            triage_priority TEXT NOT NULL,
            triage_confidence REAL NOT NULL,
            consultation_status TEXT NOT NULL DEFAULT 'Waiting for doctor consultation',
            doctor_notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    # Ensure demo doctor exists for easy testing if needed
    cursor.execute("SELECT id FROM doctors WHERE doctor_id = 'DOC-101' OR email = 'doctor@kiosk.in'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO doctors (doctor_id, full_name, email, phone_number, password_hash)
            VALUES (?, ?, ?, ?, ?)
        """, ('DOC-101', 'Dr. Arvind Sharma', 'doctor@kiosk.in', '9876543210', hash_password('doctor123')))

    conn.commit()
    conn.close()

def generate_patient_id() -> str:
    """Generate unique readable patient ID (e.g., PAT-2026-8472)."""
    random_digits = "".join(random.choices(string.digits, k=4))
    year = datetime.now().year
    return f"PAT-{year}-{random_digits}"

def generate_consultation_id() -> str:
    """Generate unique readable consultation ID (e.g., CNS-2026-9134)."""
    random_digits = "".join(random.choices(string.digits, k=4))
    year = datetime.now().year
    return f"CNS-{year}-{random_digits}"

def register_patient_account(full_name: str, age: int, gender: str, phone_number: str, 
                             preferred_language: str, location: str = "", password: str = "") -> str:
    """Register a new patient account with credentials."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    patient_id = generate_patient_id()
    while True:
        cursor.execute("SELECT id FROM patients WHERE patient_id = ?", (patient_id,))
        if not cursor.fetchone():
            break
        patient_id = generate_patient_id()

    p_hash = hash_password(password) if password else ""

    cursor.execute("""
        INSERT INTO patients (patient_id, full_name, age, gender, phone_number, preferred_language, location, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (patient_id, full_name.strip(), int(age), gender.strip(), phone_number.strip(), preferred_language.strip(), location.strip(), p_hash))

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

def register_doctor_account(full_name: str, email: str, doctor_id: str, phone_number: str, password: str) -> str:
    """Register a new doctor account."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    doc_id = doctor_id.strip() if doctor_id.strip() else f"DOC-{random.randint(100, 999)}"
    p_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO doctors (doctor_id, full_name, email, phone_number, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (doc_id, full_name.strip(), email.strip().lower(), phone_number.strip(), p_hash))

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

def create_consultation(patient_id: str, symptoms_text: str, detected_symptoms: str, 
                        triage_priority: str, triage_confidence: float) -> str:
    """Create a new triage/consultation record."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    consultation_id = generate_consultation_id()
    while True:
        cursor.execute("SELECT id FROM consultations WHERE consultation_id = ?", (consultation_id,))
        if not cursor.fetchone():
            break
        consultation_id = generate_consultation_id()

    cursor.execute("""
        INSERT INTO consultations (
            consultation_id, patient_id, symptoms_text, detected_symptoms, 
            triage_priority, triage_confidence, consultation_status
        ) VALUES (?, ?, ?, ?, ?, ?, 'Waiting for doctor consultation')
    """, (consultation_id, patient_id, symptoms_text, detected_symptoms, triage_priority, float(triage_confidence)))

    conn.commit()
    conn.close()
    return consultation_id

def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
    """Fetch patient details by patient_id."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_consultation_by_id(consultation_id: str) -> Optional[Dict[str, Any]]:
    """Fetch consultation details by consultation_id."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, p.full_name, p.age, p.gender, p.phone_number, p.preferred_language, p.location
        FROM consultations c
        JOIN patients p ON c.patient_id = p.patient_id
        WHERE c.consultation_id = ?
    """, (consultation_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_consultations() -> List[Dict[str, Any]]:
    """Retrieve all consultations ordered by priority urgency and time."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.id,
            c.consultation_id,
            c.patient_id,
            p.full_name,
            p.age,
            p.gender,
            p.phone_number,
            p.preferred_language,
            p.location,
            c.symptoms_text,
            c.detected_symptoms,
            c.triage_priority,
            c.triage_confidence,
            c.consultation_status,
            c.doctor_notes,
            c.created_at,
            c.updated_at
        FROM consultations c
        JOIN patients p ON c.patient_id = p.patient_id
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

def update_consultation_status(consultation_id: str, new_status: str):
    """Update consultation status."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE consultations
        SET consultation_status = ?, updated_at = ?
        WHERE consultation_id = ?
    """, (new_status, now, consultation_id))
    conn.commit()
    conn.close()

def update_doctor_notes(consultation_id: str, notes: str):
    """Save doctor clinical notes."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE consultations
        SET doctor_notes = ?, updated_at = ?
        WHERE consultation_id = ?
    """, (notes, now, consultation_id))
    conn.commit()
    conn.close()

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

    conn.close()
    return {
        "total_patients": total_patients,
        "waiting": waiting,
        "in_progress": in_progress,
        "urgent_pending": urgent
    }
