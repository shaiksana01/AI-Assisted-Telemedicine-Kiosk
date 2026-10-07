"""
Prescription REST API endpoints for AI-Assisted Telemedicine Kiosk.
"""

from flask import Blueprint, request, jsonify, make_response
import database.database as db
from backend.services.prescription_service import generate_prescription_html

prescription_bp = Blueprint("prescription_bp", __name__, url_prefix="/api/prescriptions")

@prescription_bp.route("", methods=["POST"])
def create_prescription():
    data = request.get_json() or {}
    consultation_id = data.get("consultation_id")
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    medicines = data.get("medicines", [])
    general_notes = data.get("general_notes", "")

    if not consultation_id or not patient_id or not doctor_id:
        return jsonify({"success": False, "error": "consultation_id, patient_id, and doctor_id are required."}), 400

    rx_id = db.create_prescription(
        consultation_id=consultation_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        medicines=medicines,
        general_notes=general_notes
    )

    rx = db.get_prescription_by_consultation_id(consultation_id)
    return jsonify({"success": True, "prescription_id": rx_id, "prescription": rx}), 201

@prescription_bp.route("/consultation/<consultation_id>", methods=["GET"])
def get_by_consultation(consultation_id):
    rx = db.get_prescription_by_consultation_id(consultation_id)
    if not rx:
        return jsonify({"success": False, "error": "No prescription found for this consultation."}), 404
    return jsonify({"success": True, "prescription": rx}), 200

@prescription_bp.route("/<consultation_id>/html", methods=["GET"])
def get_prescription_document(consultation_id):
    rx = db.get_prescription_by_consultation_id(consultation_id)
    if not rx:
        return jsonify({"success": False, "error": "Prescription not found."}), 404

    cns = db.get_consultation_by_id(consultation_id)
    patient = db.get_patient_by_id(rx["patient_id"]) or {}
    doctor = db.get_doctor_by_id(rx["doctor_id"]) or {}

    html_content = generate_prescription_html(rx, patient, doctor)
    response = make_response(html_content)
    response.headers["Content-Type"] = "text/html"
    return response
