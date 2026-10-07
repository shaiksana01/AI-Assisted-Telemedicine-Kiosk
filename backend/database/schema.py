"""
SQLAlchemy Schema Models for AI-Assisted Telemedicine Kiosk.
Defines normalized entities for Patients, Doctors, Consultations, Triage Results, Prescriptions, and EHR.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    phone_number = Column(String(20), nullable=False, index=True)
    email = Column(String(120), default="")
    preferred_language = Column(String(50), default="English")
    location = Column(String(150), default="")
    password_hash = Column(String(256), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    consultations = relationship("Consultation", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    specialization = Column(String(100), default="General Medicine")
    license_number = Column(String(100), default="")
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    password_hash = Column(String(256), nullable=False)
    preferred_language = Column(String(50), default="English")
    created_at = Column(DateTime, default=datetime.utcnow)

    consultations = relationship("Consultation", back_populates="doctor")

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_id = Column(String(50), unique=True, nullable=False, index=True)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False, index=True)
    doctor_id = Column(String(50), ForeignKey("doctors.doctor_id"), default="", nullable=True)
    symptoms_text = Column(Text, nullable=False)
    detected_symptoms = Column(Text, nullable=False)
    triage_priority = Column(String(50), nullable=False)
    triage_confidence = Column(Float, nullable=False)
    consultation_status = Column(String(50), default="Waiting for doctor consultation", index=True)
    chief_complaint = Column(Text, default="")
    doctor_notes = Column(Text, default="")
    doctor_observations = Column(Text, default="")
    doctor_advice = Column(Text, default="")
    follow_up_recommendation = Column(Text, default="")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
    prescription = relationship("Prescription", back_populates="consultation", uselist=False)

class SymptomRecord(Base):
    __tablename__ = "symptom_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_id = Column(String(50), ForeignKey("consultations.consultation_id"), nullable=False)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    raw_symptom_text = Column(Text, nullable=False)
    input_method = Column(String(20), default="text")
    detected_symptoms_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)

class TriageResult(Base):
    __tablename__ = "triage_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_id = Column(String(50), ForeignKey("consultations.consultation_id"), nullable=False)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    predicted_priority = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    feature_vector_json = Column(Text, default="{}")
    probabilities_json = Column(Text, default="{}")
    explanation = Column(Text, default="")
    is_emergency = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(String(50), unique=True, nullable=False, index=True)
    consultation_id = Column(String(50), ForeignKey("consultations.consultation_id"), nullable=False)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String(50), ForeignKey("doctors.doctor_id"), nullable=False)
    general_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    consultation = relationship("Consultation", back_populates="prescription")
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")

class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(String(50), ForeignKey("prescriptions.prescription_id"), nullable=False)
    medicine_name = Column(String(150), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)
    instructions = Column(Text, default="")

    prescription = relationship("Prescription", back_populates="items")
