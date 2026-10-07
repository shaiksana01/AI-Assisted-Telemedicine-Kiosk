"""
Authentication REST API endpoints for Patients and Doctors.
"""

from flask import Blueprint, request, jsonify
import database.database as db
from backend.auth.auth_service import validate_patient_registration, validate_doctor_registration

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

@auth_bp.route("/patient/register", methods=["POST"])
def patient_register():
    data = request.get_json() or {}
    is_valid, err = validate_patient_registration(data)
    if not is_valid:
        return jsonify({"success": False, "error": err}), 400

    try:
        patient_id = db.register_patient_account(
            full_name=data.get("full_name"),
            age=int(data.get("age")),
            gender=data.get("gender"),
            phone_number=data.get("phone_number"),
            preferred_language=data.get("preferred_language", "English"),
            location=data.get("location", ""),
            password=data.get("password", ""),
            email=data.get("email", "")
        )
        patient = db.get_patient_by_id(patient_id)
        return jsonify({"success": True, "patient_id": patient_id, "patient": patient}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route("/patient/login", methods=["POST"])
def patient_login():
    data = request.get_json() or {}
    phone = data.get("phone_number", "").strip()
    password = data.get("password", "")

    if not phone:
        return jsonify({"success": False, "error": "Phone number is required."}), 400

    patient = db.authenticate_patient(phone, password)
    if not patient:
        return jsonify({"success": False, "error": "Invalid phone number or password."}), 401

    return jsonify({"success": True, "patient": patient}), 200

@auth_bp.route("/doctor/register", methods=["POST"])
def doctor_register():
    data = request.get_json() or {}
    is_valid, err = validate_doctor_registration(data)
    if not is_valid:
        return jsonify({"success": False, "error": err}), 400

    try:
        doctor_id = db.register_doctor_account(
            full_name=data.get("full_name"),
            email=data.get("email"),
            doctor_id=data.get("doctor_id", ""),
            phone_number=data.get("phone_number"),
            password=data.get("password"),
            specialization=data.get("specialization", "General Medicine"),
            license_number=data.get("license_number", ""),
            preferred_language=data.get("preferred_language", "English")
        )
        doctor = db.get_doctor_by_id(doctor_id)
        return jsonify({"success": True, "doctor_id": doctor_id, "doctor": doctor}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@auth_bp.route("/doctor/login", methods=["POST"])
def doctor_login():
    data = request.get_json() or {}
    id_or_email = data.get("id_or_email", "").strip()
    password = data.get("password", "")

    if not id_or_email or not password:
        return jsonify({"success": False, "error": "Doctor ID/Email and password are required."}), 400

    doctor = db.authenticate_doctor(id_or_email, password)
    if not doctor:
        return jsonify({"success": False, "error": "Invalid credentials."}), 401

    return jsonify({"success": True, "doctor": doctor}), 200
