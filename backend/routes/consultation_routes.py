"""
Consultation REST API endpoints for AI-Assisted Telemedicine Kiosk.
"""

from flask import Blueprint, request, jsonify
import database.database as db
from backend.services.consultation_service import get_waiting_queue, get_active_consultations, get_completed_consultations

consultation_bp = Blueprint("consultation_bp", __name__, url_prefix="/api/consultations")

@consultation_bp.route("", methods=["GET"])
def list_consultations():
    status_filter = request.args.get("status")
    if status_filter == "waiting":
        consultations = get_waiting_queue()
    elif status_filter == "active":
        consultations = get_active_consultations()
    elif status_filter == "completed":
        consultations = get_completed_consultations()
    else:
        consultations = db.get_all_consultations()
    return jsonify({"success": True, "consultations": consultations}), 200

@consultation_bp.route("/<consultation_id>", methods=["GET"])
def get_consultation(consultation_id):
    cns = db.get_consultation_by_id(consultation_id)
    if not cns:
        return jsonify({"success": False, "error": "Consultation not found."}), 404
    return jsonify({"success": True, "consultation": cns}), 200

@consultation_bp.route("", methods=["POST"])
def create_new_consultation():
    data = request.get_json() or {}
    patient_id = data.get("patient_id")
    symptoms_text = data.get("symptoms_text", "")
    detected_symptoms = data.get("detected_symptoms", "")
    triage_priority = data.get("triage_priority", "Moderate Priority")
    triage_confidence = float(data.get("triage_confidence", 0.85))
    input_method = data.get("input_method", "text")
    triage_metadata = data.get("triage_metadata")

    if not patient_id:
        return jsonify({"success": False, "error": "patient_id is required."}), 400

    cid = db.create_consultation(
        patient_id=patient_id,
        symptoms_text=symptoms_text,
        detected_symptoms=detected_symptoms,
        triage_priority=triage_priority,
        triage_confidence=triage_confidence,
        input_method=input_method,
        triage_metadata=triage_metadata
    )
    return jsonify({"success": True, "consultation_id": cid}), 201

@consultation_bp.route("/<consultation_id>/status", methods=["PATCH"])
def update_status(consultation_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    doctor_id = data.get("doctor_id")

    if not new_status:
        return jsonify({"success": False, "error": "status is required."}), 400

    db.update_consultation_status(consultation_id, new_status, doctor_id)
    return jsonify({"success": True, "message": "Status updated successfully."}), 200

@consultation_bp.route("/<consultation_id>/notes", methods=["POST", "PUT"])
def update_notes(consultation_id):
    data = request.get_json() or {}
    notes = data.get("notes", "")
    chief_complaint = data.get("chief_complaint", "")
    observations = data.get("observations", "")
    advice = data.get("advice", "")
    followup = data.get("followup", "")

    db.update_doctor_notes(
        consultation_id=consultation_id,
        notes=notes,
        chief_complaint=chief_complaint,
        observations=observations,
        advice=advice,
        followup=followup
    )
    return jsonify({"success": True, "message": "Clinical notes updated."}), 200
