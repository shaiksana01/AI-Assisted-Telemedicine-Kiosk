"""
Patient and Doctor REST API endpoints.
"""

from flask import Blueprint, request, jsonify
import database.database as db
from backend.services.ehr_service import get_complete_patient_history

patient_bp = Blueprint("patient_bp", __name__, url_prefix="/api/patients")
doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/api/doctors")

# --- Patient Endpoints ---
@patient_bp.route("/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = db.get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"success": False, "error": "Patient not found."}), 404
    # Sanitize password hash before returning
    patient.pop("password_hash", None)
    return jsonify({"success": True, "patient": patient}), 200

@patient_bp.route("/<patient_id>/ehr", methods=["GET"])
def get_patient_ehr_endpoint(patient_id):
    ehr = get_complete_patient_history(patient_id)
    if not ehr:
        return jsonify({"success": False, "error": "No EHR history found for this patient."}), 404
    if "patient" in ehr:
        ehr["patient"].pop("password_hash", None)
    return jsonify({"success": True, "ehr": ehr}), 200

# --- Doctor Endpoints ---
@doctor_bp.route("/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = db.get_doctor_by_id(doctor_id)
    if not doctor:
        return jsonify({"success": False, "error": "Doctor not found."}), 404
    doctor.pop("password_hash", None)
    return jsonify({"success": True, "doctor": doctor}), 200

@doctor_bp.route("/queue/stats", methods=["GET"])
def get_stats():
    stats = db.get_queue_summary_stats()
    return jsonify({"success": True, "stats": stats}), 200
